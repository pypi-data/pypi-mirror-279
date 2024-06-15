from importlib.resources import files
from pathlib import Path

import numpy as np
import pandas as pd
import xarray as xr
from periodictable import formula as pt_formula
from scipy.interpolate import interp1d

from pyxro.defaults import BINDING_ENERGIES_LIST


def imfp(layer_data, ke):
    nval = layer_data.num_valence_electrons.to_numpy()
    dens = layer_data.density.to_numpy()
    molw = layer_data.molecular_weight.to_numpy()
    egap = layer_data.energy_gap.to_numpy()
    temp1 = 829.44 * nval * dens / molw
    temp2 = 0.191 / np.sqrt(dens)
    temp3 = 1.97 - 0.91 * temp1 / 829.4
    temp4 = 53.4 - 20.8 * temp1 / 829.4
    temp5 = np.sqrt(temp1 + egap**2)
    temp5 = -0.1 + 0.944 / temp5 + 0.069 * (dens) ** 0.1
    return ke / (temp1 * (temp5 * np.log(temp2 * ke) - temp3 / ke + temp4 / (ke * ke)))


def new_imfp(layer_data, ke):
    nval = layer_data.num_valence_electrons.to_numpy()
    dens = layer_data.density.to_numpy()
    molw = layer_data.molecular_weight.to_numpy()
    egap = layer_data.energy_gap.to_numpy()
    temp1 = 829.44 * nval * dens / molw
    temp2 = 0.191 / np.sqrt(dens)
    temp3 = 1.97 - 0.91 * temp1 / 829.4
    temp4 = 53.4 - 20.8 * temp1 / 829.4
    temp5 = np.sqrt(temp1 + egap**2)
    temp5 = -0.1 + 0.944 / temp5 + 0.069 * (dens) ** 0.1
    return ke / (temp1 * (temp5 * np.log(temp2 * ke) - temp3 / ke + temp4 / (ke * ke)))


def ncos(angle, ior):
    Y = 2.0 * ior.real * ior.imag
    X = ior.real**2 - ior.imag**2 - np.sin(angle) ** 2
    sqrt_term = np.sqrt(X**2 + Y**2)
    real_term = np.sqrt((X + sqrt_term) / 2)
    imag_term = np.sqrt((-X + sqrt_term) / 2)
    return real_term + 1j * imag_term


def calculate_interdiffusion(f, c, d):
    match f:
        case "none":
            return 1.0 * np.ones_like(c)
        case "mean":
            t = c**2 * d**2 / 2
            return np.exp(-t.astype(complex))
        case "linear":
            t = c**2 * d**2 / 2
            return np.exp(-t.astype(complex))
        case "circular":
            t = c**2 * d**2 / 2
            return 1.0 / (1.0 + t.astype(complex))
        case "parabola":
            t = np.sqrt(3) * d * c
            t = t.astype(complex)
            t3 = np.sin(t.real) * np.cosh(t.imag)
            t4 = np.cos(t.real) * np.sinh(t.imag)
            return (t3 + 1j * t4) / t
        case "trapezoid":
            t = (np.pi / np.sqrt(np.pi**2 - 8.0)) * d * c
            t = t.astype(complex)
            t4 = np.cos(t.real) * np.cosh(t.imag)
            t5 = np.sin(t.real) * np.sinh(t.imag)
            return np.pi * np.pi * (t4 - 1j * t5) / (np.pi**2 / 4.0 - t * t) / 4.0


def mix(x, t, d, a, b, m):
    F = x
    match t:
        case "none":
            F = x
        case "mean":
            F = x / 2
        case "linear":
            match m:
                case 1:
                    F = 0.5 * x * ((d - a) / b + 1)
                case 2:
                    F = x * (1 - (d - a + b) / (2 * b))
                case 3:
                    F = 0.5 * x * (-(d - a) / b + 1)
                case 4:
                    F = x * (d - a + b) / (2 * b)
        case "circular":
            match m:
                case 1:
                    F = x * np.sqrt(1 - (d - a - b) ** 2 / (4 * b**2))
                case 2:
                    F = x * np.sqrt(1 - (d - a + b) ** 2 / (4 * b**2))
                case 3:
                    F = x * np.sqrt(1 - (d - a + b) ** 2 / (4 * b**2))
                case 4:
                    F = x * np.sqrt(1 - (d - a - b) ** 2 / (4 * b**2))
        case "parabola":
            match m:
                case 1:
                    F = x * (-(((d - a - b) / (2 * b)) ** 2) + 1)
                case 2:
                    F = x * (-(((d - a + b) / (2 * b)) ** 2) + 1)
                case 3:
                    F = x * (-(((d - a + b) / (2 * b)) ** 2) + 1)
                case 4:
                    F = x * (-(((d - a - b) / (2 * b)) ** 2) + 1)
        case "trapezoid":
            match m:
                case 1:
                    F = x * (-(((d - a - b) / (2 * b)) ** 2) + 1)
                case 2:
                    F = x * (-(((d - a + b) / (2 * b)) ** 2) + 1)
                case 3:
                    F = x * (-(((d - a + b) / (2 * b)) ** 2) + 1)
                case 4:
                    F = x * (-(((d - a - b) / (2 * b)) ** 2) + 1)

    return F


def gausstail(x, a1, a2, s1, s2):
    sw1 = s1 * np.sqrt(np.log(2))
    sw2 = s2 * np.sqrt(np.log(2))
    if x < a1:
        F = np.exp(-(((x - a1) / sw1) ** 2))
    elif x >= a1 and x <= a2:
        F = 1
    else:
        F = np.exp(-(((x - a2) / sw2) ** 2))

    return F


class Calculation:
    def __init__(self, sample):
        self.sample = sample
        self.rcs = pd.DataFrame(sample.input["rocking_curves"])
        self.depth_mesh = sample.input["setup"]["integral_mesh"]
        self.inbetween_angle = sample.input["setup"]["inbetween_angle"]
        self.light_polarization = sample.input["setup"]["light_polarization"]
        self.scan_mode = sample.input["setup"]["scan_mode"]

        # Vacuum + all layers + substrate
        self.minisample = pd.DataFrame(sample.input["layers"])
        self.fullsample = sample.get_fullsample()
        self.n_of_layers = self.fullsample.shape[0]
        self.layer_ids = self.fullsample["id"].values
        self.layer_indexes = self.fullsample.index.values
        self.thicknesses = self.fullsample["thickness"].values
        self.interdiffusion = self.fullsample["interdiffusion"].values
        self.interdiffusion_type = self.fullsample["interdiffusion_type"].values

        # Layer atoms info
        self.layer_atoms = (
            self.fullsample[:-1]
            .apply(
                lambda r: {k.symbol: v for k, v in pt_formula(r.formula).atoms.items()},
                axis=1,
            )
            .values
        )
        self.minilayer_atoms = (
            self.minisample[:-1]
            .apply(
                lambda r: {k.symbol: v for k, v in pt_formula(r.formula).atoms.items()},
                axis=1,
            )
            .values
        )

        # Axes
        self.incident_angles = sample.get_angle_axis()
        self.photon_energies = sample.get_energy_axis()
        self.wavenumbers = 12399.554 / self.photon_energies
        self.conv_incident_angles = np.radians(90.0 - self.incident_angles)

        # Index of refraction
        self.ior = sample.opc.to_numpy()  # ior = (1-delta) + i*beta
        self.ior = (1 - self.ior.real) + 1j * self.ior.imag  # ior = alpha + i*beta
        self.full_ior = np.array([self.ior[:, c] for c in self.layer_ids]).T

    def set_reflectivity(self):
        if not hasattr(self, "fresnel_r"):
            self.set_fresnel_coefficients()

        Chi = (
            2
            * np.pi
            * self.P
            * np.array(
                self.thicknesses[None, None, :] / self.wavenumbers[None, :, None],
                dtype=complex,
            )
        )
        Ph = np.exp(2 * 1j * Chi)
        # Compute the reflection coefficient for each layer interface and
        # propagate it through the sample to obtain the total reflection
        # coefficient. `re` represents the reflection coefficient at each
        # interface, and `Reflectivity` is the total reflection coefficient.
        re = np.zeros_like((len(self.conv_incident_angles), len(self.wavenumbers)))
        re_prev = self.fresnel_r[:, :, -1]
        for l_curr, l_next in zip(
            self.layer_indexes[1:-1][::-1], self.layer_indexes[:-2][::-1]
        ):
            r1 = re_prev * Ph[:, :, l_curr]
            r3 = self.fresnel_r[:, :, l_next] * r1
            re = (self.fresnel_r[:, :, l_next] + r1) / (1 + r3)
            re_prev = re

        re = re * re.conjugate()
        self.reflectivity = xr.DataArray(
            data=re.real,
            name="reflectivity",
            coords={
                "angle": self.incident_angles,
                "energy": self.photon_energies,
            },
            dims=["angle", "energy"],
            attrs={
                "scan_mode": self.scan_mode,
            },
        )

    def set_terms(self):
        self.P = ncos(self.conv_incident_angles[:, None, None], self.full_ior[None, :])
        self.G = self.P / self.full_ior
        self.S = (
            np.sin(self.conv_incident_angles[:, None, None]) / self.full_ior[None, :]
        )

    def set_fresnel_coefficients(self):
        if any(not hasattr(self, attr) for attr in ["P", "G"]):
            self.set_terms()

        fresnel_r = np.zeros(
            (
                len(self.conv_incident_angles),
                len(self.wavenumbers),
                self.n_of_layers - 1,
            ),
            dtype=complex,
        )
        fresnel_t = np.zeros(
            (
                len(self.conv_incident_angles),
                len(self.wavenumbers),
                self.n_of_layers - 1,
            ),
            dtype=complex,
        )
        for l_curr, l_next in zip(self.layer_indexes, self.layer_indexes[1:]):
            tmp_diff = (
                4 * np.pi * self.G[:, :, [l_curr]] / self.wavenumbers[None, :, None]
            )
            tmp_mult = calculate_interdiffusion(
                self.interdiffusion_type[None, None, [l_curr]],
                tmp_diff,
                self.interdiffusion[None, None, [l_curr]],
            )

            if self.light_polarization == "s":
                fresnel_r[:, :, [l_curr]] = (
                    tmp_mult
                    * (self.P[:, :, [l_curr]] - self.P[:, :, [l_next]])
                    / (self.P[:, :, [l_curr]] + self.P[:, :, [l_next]])
                )
                fresnel_t[:, :, [l_curr]] = (
                    2.0
                    * self.P[:, :, [l_curr]]
                    / (self.P[:, :, [l_curr]] + self.P[:, :, [l_next]])
                )
            else:
                tmp_a = self.full_ior[:, [l_curr]] * self.G[:, :, [l_next]]
                tmp_b = self.full_ior[:, [l_next]] * self.G[:, :, [l_curr]]
                fresnel_r[:, :, [l_curr]] = tmp_mult * (tmp_a - tmp_b) / (tmp_a + tmp_b)
                fresnel_t[:, :, [l_curr]] = (
                    2.0 * self.P[:, :, [l_curr]] / (tmp_a + tmp_b)
                )
        fresnel_t[fresnel_t == 0] = 1e-15 * (1 + 1j)

        self.fresnel_r = fresnel_r
        self.fresnel_t = fresnel_t

    def set_fields(self):
        if any(not hasattr(self, attr) for attr in ["fresnel_r", "fresnel_t"]):
            self.set_fresnel_coefficients()

        k = 0
        Chi = 2 * np.pi * self.P / self.wavenumbers[:, None]
        z_grouped_list = [
            np.linspace(0.0, self.thicknesses[i], self.depth_mesh + 1)
            for i in self.layer_indexes[:-1]
        ]
        self.incident_field = np.zeros(
            (
                len(self.conv_incident_angles),
                len(self.wavenumbers),
                (self.n_of_layers - 1) * self.depth_mesh + 1,
            ),
            dtype=complex,
        )
        self.reflected_field = np.zeros(
            (
                len(self.conv_incident_angles),
                len(self.wavenumbers),
                (self.n_of_layers - 1) * self.depth_mesh + 1,
            ),
            dtype=complex,
        )
        for i, l_idx in enumerate(self.layer_indexes[:-1][::-1]):
            if i > 0:
                incident_field_prev = self.incident_field[:, :, [k]]
                reflected_field_prev = self.reflected_field[:, :, [k]]
            else:
                incident_field_prev = np.ones_like(self.incident_field[:, :, [0]])
                reflected_field_prev = np.zeros_like(incident_field_prev)

            for j in range(self.depth_mesh + 1):
                Chi_times_z = Chi[:, :, [l_idx]] * z_grouped_list[l_idx][j]
                pp = np.exp(-1j * Chi_times_z)
                pn = np.exp(1j * Chi_times_z)

                ep_t1 = pp / self.fresnel_t[:, :, [l_idx]]
                ep_t2 = ep_t1 * self.fresnel_r[:, :, [l_idx]]
                self.incident_field[:, :, [k]] = (
                    ep_t1 * incident_field_prev + ep_t2 * reflected_field_prev
                )

                en_t1 = pn / self.fresnel_t[:, :, [l_idx]]
                en_t2 = en_t1 * self.fresnel_r[:, :, [l_idx]]
                self.reflected_field[:, :, [k]] = (
                    en_t2 * incident_field_prev + en_t1 * reflected_field_prev
                )

                if j < self.depth_mesh:
                    k += 1
        self.z_slices = k

    def set_field_amplitudes(self):
        if any(
            not hasattr(self, attr) for attr in ["incident_field", "reflected_field"]
        ):
            self.set_fields()

        k = self.z_slices

        t1 = (
            self.fresnel_r[:, :, [0]]
            * self.reflected_field[:, :, [k - self.depth_mesh - 1]]
        )
        p0 = np.divide(
            self.incident_field[:, :, [k - self.depth_mesh - 1]],
            self.fresnel_t[:, :, [0]],
        ) + np.divide(t1, self.fresnel_t[:, :, [0]])
        T = np.abs(1 / p0) ** 2

        intensities = []
        z = 0
        layer = 0
        pz = np.zeros(k + 1)
        dz_list = [
            self.thicknesses[i] / self.depth_mesh for i in self.layer_indexes[:-1]
        ]
        # l_list = np.array([int(np.fix(i/self.depth_mesh)) \
        # if i<k else int(np.fix((k-1)/self.depth_mesh)) for i in range(k+1)])
        for i in range(k + 1):
            if self.light_polarization == "s":
                tmp = (
                    T
                    * np.abs(
                        self.incident_field[:, :, [k - i]]
                        + self.reflected_field[:, :, [k - i]]
                    )
                    ** 2
                )
            else:
                It = (
                    T
                    * np.abs(
                        self.incident_field[:, :, [k - i]]
                        + self.reflected_field[:, :, [k - i]]
                    )
                    ** 2
                    * np.abs(self.G[:, :, [layer]]) ** 2
                )
                In = (
                    T
                    * np.abs(
                        self.incident_field[:, :, [k - i]]
                        - self.reflected_field[:, :, [k - i]]
                    )
                    ** 2
                    * np.abs(self.S[:, :, [layer]]) ** 2
                )
                tmp = It + In

            intensities.append(tmp.astype(np.float64))
            pz[i] = z - self.thicknesses[0]
            if i < k:
                layer = int(np.fix(i / self.depth_mesh))
                z = z + dz_list[layer]

        self.dz_list = dz_list
        self.z_values = pz
        self.field_amplitudes = np.dstack(intensities)
        self.electric_field = xr.DataArray(
            data=self.field_amplitudes,
            name="electric_field",
            coords={
                "angle": self.incident_angles,
                "energy": self.photon_energies,
                "depth": self.z_values,
            },
            dims=["angle", "energy", "depth"],
            attrs={
                "scan_mode": self.scan_mode,
            },
        )

    def get_orbital_data(self, Ank):
        if Ank is None:
            return
        element, orbital = Ank[:-2], Ank[-2:]
        file = files("pyxro.data.acs").joinpath(f"{element}.csv")
        if not file.is_file():
            return
        filedata = pd.read_csv(file, header=[0, 1], index_col=0)
        acsdata = filedata[orbital].dropna()
        acs = interp1d(acsdata.index.values, acsdata.x.values)
        asp = 2 * np.ones_like(self.photon_energies)
        return acs(self.photon_energies), asp

    def get_single_photoemission(self, label=None, Ank=None, layers=[]):
        if any(
            not hasattr(self, attr)
            for attr in ["field_amplitudes", "z_values", "dz_list"]
        ):
            self.set_field_amplitudes()
        if Ank is None or len(layers) == 0:
            return
        if label is None:
            label = Ank
        element, orbital = Ank[:-2], Ank[-2:]

        full_layers = self.layer_indexes[
            np.argwhere(np.isin(self.layer_ids, layers)).ravel()
        ]

        binding_energy = BINDING_ENERGIES_LIST.loc[element, orbital]

        # Same values for every layer in layers
        acs, asp = self.get_orbital_data(Ank)
        acs = acs[np.newaxis, :, np.newaxis]
        asp = asp[np.newaxis, :, np.newaxis]

        # For a subshell Ak, this is the A_{Ak} term that is a function of the
        # assymetry parameter \eta_{Ak} and the angle \csi_{Ak} between the
        # polarization direction and the electron emission direction:
        # A_{Ak} = [1 + \eta_{Ak}(3*g/2 - 1/2)], where g = cos^2(\eta_{Ak})
        #
        #
        match self.light_polarization:
            case "p":
                gam = np.cos(np.radians(abs(self.inbetween_angle - 90))) ** 2
            case "s+p?":  # check this
                gam = np.cos(np.radians(self.inbetween_angle)) ** 2
            case "s" | _:
                gam = 0.0

        ay = np.zeros(
            (self.incident_angles.size, self.photon_energies.size, self.n_of_layers - 1)
        )
        nay = np.zeros(
            (self.incident_angles.size, self.photon_energies.size, self.n_of_layers - 1)
        )
        atom_density = (
            self.fullsample[:-1]
            .apply(
                lambda r: (
                    r.density * self.layer_atoms[r.id][element] / r.molecular_weight
                    if r.molecular_weight > 0 and r.id in layers
                    else 0
                ),
                axis=1,
            )
            .values
        )

        nay[:, :, full_layers] = (1 + asp * (3 * gam - 1) / 2) * atom_density[
            full_layers
        ]
        ay[:, :, full_layers] = nay[:, :, full_layers] * acs

        # Back reflection of photoelectrons
        RE = np.zeros((self.incident_angles.size, self.photon_energies.size))
        tp = np.zeros((self.incident_angles.size, self.photon_energies.size))
        tffag = self.incident_angles.copy()
        tffag += self.inbetween_angle
        tffag[tffag >= 90] = 180 - tffag[tffag >= 90]
        scattering_angles = np.linspace(0, 90, 9001)
        sin_sqr_scatt_angles = np.sin(np.radians(scattering_angles)) ** 2
        for ii in range(len(self.incident_angles)):
            for jj, photon_energy in enumerate(self.photon_energies):
                kinetic_energy = photon_energy - binding_energy
                if kinetic_energy <= 15.0:
                    RE[ii, jj] = 0.0
                    tp[ii, jj] = 90
                else:
                    if abs(tffag[ii] - 90.0) < 1e-5:
                        tp[ii, jj] = 90
                        t1 = np.sqrt(1.0 - 15.0 / kinetic_energy)
                        t2 = (1 - t1) / (1 + t1)
                        RE[ii, jj] = t2**2
                    else:
                        first_test = np.argwhere(
                            sin_sqr_scatt_angles >= 15.0 / kinetic_energy
                        ).squeeze()[0]
                        values = np.degrees(
                            np.arctan(
                                np.sqrt(
                                    sin_sqr_scatt_angles[first_test:]
                                    - 15.0 / kinetic_energy
                                )
                                / np.cos(np.radians(scattering_angles[first_test:]))
                            )
                        )
                        best_value = np.argwhere(tffag[ii] <= values).squeeze()[0]
                        tp[ii, jj] = scattering_angles[first_test + best_value]
                        t1 = np.sin(np.radians(tp[ii, jj])) ** 2
                        t2 = np.sqrt(1.0 - 15.0 / (kinetic_energy * t1))
                        t3 = (1.0 - t2) / (1.0 + t2)
                        RE[ii, jj] = t3**2

        RE = 1 - RE

        # Effective attenuation length of the photoelectrons
        # This depends on the binding energy of the subshell
        attenuation_length_by_layer = np.zeros(
            (self.photon_energies.size, self.n_of_layers - 1)
        )
        attenuation_length_by_layer[:, 0] = 1e100
        attenuation = np.zeros(
            (
                self.incident_angles.size,
                self.photon_energies.size,
                (self.n_of_layers - 1) * self.depth_mesh + 1,
            )
        )
        attenuation_length = np.zeros(
            (
                self.incident_angles.size,
                self.photon_energies.size,
                (self.n_of_layers - 1) * self.depth_mesh + 1,
            )
        )
        for jj, photon_energy in enumerate(self.photon_energies):
            kinetic_energy = photon_energy - binding_energy
            for j, l_idx in zip(self.layer_ids[1:-1], self.layer_indexes[1:-1]):
                selected_sample = self.minisample[self.minisample["id"].isin([j])]
                attenuation_length_by_layer[jj, l_idx] = new_imfp(
                    selected_sample, kinetic_energy
                )
        h = 0
        for i, l_idx in enumerate(self.layer_indexes[:-1][::-1]):
            for j in range(self.depth_mesh + 1):
                attenuation_length[:, :, h] = attenuation_length_by_layer[:, l_idx]
                dz = self.dz_list[l_idx]
                attenuation[:, :, h] = np.exp(
                    -dz
                    / (attenuation_length_by_layer[:, l_idx] * np.sin(np.radians(tp)))
                )
                if j < self.depth_mesh:
                    h = h + 1

        accthick = np.zeros(self.n_of_layers)
        for i, row_data in self.fullsample.iloc[1:, :].iterrows():
            accthick[i] = accthick[i - 1] + self.fullsample.iloc[i - 1].thickness
        paccthick = accthick - self.fullsample.iloc[0].thickness

        phI = np.zeros(
            (
                self.incident_angles.size,
                self.photon_energies.size,
                (self.n_of_layers - 1) * self.depth_mesh + 1,
            )
        )
        phimfp = np.zeros(
            (
                self.incident_angles.size,
                self.photon_energies.size,
                (self.n_of_layers - 1) * self.depth_mesh + 1,
            )
        )
        spotsize = 1
        spotsize_correction = 1
        layer = 0
        k = self.z_slices
        tmpl = attenuation[:, :, [k]]
        l_list = np.array(
            [int(np.fix((i - 1) / self.depth_mesh)) for i in range(k + 1)]
        )
        for i, layer in zip(range(k + 1), l_list):
            if spotsize:
                spotsize_correction = 1 / np.sin(np.radians(tp[:, :, np.newaxis]))
            this_layer = int(layer in full_layers)
            next_layer = int(layer + 1 in full_layers)
            prev_layer = int(layer - 1 in full_layers)
            if i == 0 and this_layer:
                phI[:, :, [i]] = (
                    self.field_amplitudes[:, :, [i]]
                    * RE[:, :, np.newaxis]
                    * ay[:, :, [layer]]
                    * spotsize_correction
                )
                phimfp[:, :, [i]] = attenuation_length[:, :, [k - i]]
            elif i > 0:
                if (
                    layer == 0
                    and self.z_values[i]
                    > paccthick[layer + 1] - self.interdiffusion[layer]
                    and next_layer
                ):
                    phI[:, :, [i]] = (
                        self.field_amplitudes[:, :, [i]]
                        * RE[:, :, np.newaxis]
                        * mix(
                            nay[:, :, [layer + 1]],
                            self.interdiffusion_type[layer],
                            self.z_values[i],
                            paccthick[layer + 1],
                            self.interdiffusion[layer],
                            4,
                        )
                        * acs
                    )
                elif layer > 0:
                    if (
                        self.z_values[i]
                        > paccthick[layer] + self.interdiffusion[layer - 1]
                        and self.z_values[i]
                        <= paccthick[layer + 1] - self.interdiffusion[layer]
                    ):
                        phI[:, :, [i]] = (
                            self.field_amplitudes[:, :, [i]]
                            * RE[:, :, np.newaxis]
                            * ay[:, :, [layer]]
                            * this_layer
                        )
                    elif (
                        self.z_values[i]
                        <= paccthick[layer] + self.interdiffusion[layer - 1]
                        and self.z_values[i] > paccthick[layer]
                    ):
                        if this_layer:
                            phI[:, :, [i]] = (
                                self.field_amplitudes[:, :, [i]]
                                * RE[:, :, np.newaxis]
                                * mix(
                                    nay[:, :, [layer]],
                                    self.interdiffusion_type[layer - 1],
                                    self.z_values[i],
                                    paccthick[layer],
                                    self.interdiffusion[layer - 1],
                                    1,
                                )
                                * acs
                            )
                        elif this_layer and prev_layer:
                            phI[:, :, [i]] = (
                                self.field_amplitudes[:, :, [i]]
                                * RE[:, :, np.newaxis]
                                * mix(
                                    nay[:, :, [layer - 1]],
                                    self.interdiffusion_type[layer - 1],
                                    self.z_values[i],
                                    paccthick[layer],
                                    self.interdiffusion[layer - 1],
                                    3,
                                )
                                * acs
                            )
                    elif (
                        self.z_values[i] <= paccthick[layer + 1]
                        and self.z_values[i]
                        > paccthick[layer + 1] - self.interdiffusion[layer]
                    ):
                        if this_layer:
                            phI[:, :, [i]] = (
                                self.field_amplitudes[:, :, [i]]
                                * RE[:, :, np.newaxis]
                                * mix(
                                    nay[:, :, [layer]],
                                    self.interdiffusion_type[layer],
                                    self.z_values[i],
                                    paccthick[layer + 1],
                                    self.interdiffusion[layer],
                                    2,
                                )
                                * acs
                            )
                        elif this_layer and next_layer:
                            phI[:, :, [i]] = (
                                self.field_amplitudes[:, :, [i]]
                                * RE[:, :, np.newaxis]
                                * mix(
                                    nay[:, :, [layer + 1]],
                                    self.interdiffusion_type[layer],
                                    self.z_values[i],
                                    paccthick[layer + 1],
                                    self.interdiffusion[layer],
                                    4,
                                )
                                * acs
                            )

                tmpl = tmpl * attenuation[:, :, [k - i]]
                phI[:, :, [i]] = tmpl * phI[:, :, [i]] * spotsize_correction
                phimfp[:, :, [i]] = attenuation_length[:, :, [k - i]]

        # self.photoemission = xr.Dataset(
        #     data_vars = {Ank : (['angle', 'energy', 'depth'], phI)},
        #     coords = {
        #         'angle': self.incident_angles,
        #         'energy': self.photon_energies,
        #         'depth': self.z_values,
        #     },
        #     attrs = {
        #         'scan_mode' : self.scan_mode
        #     }
        # )
        self.photoemission = xr.DataArray(
            data=phI,
            name=Ank,
            coords={
                "angle": self.incident_angles,
                "energy": self.photon_energies,
                "depth": self.z_values,
            },
            dims=["angle", "energy", "depth"],
            attrs={
                "scan_mode": self.scan_mode,
            },
        )

    def export_single_photoemission(self, folder=None, filename="photoemission.nc"):
        if folder is None:
            folder = Path(self.sample.folder) / self.sample.input["folders"]["OUT"]
        else:
            folder = Path(folder)
        if not folder.is_dir():
            folder.mkdir()
        if self.photoemission is not None:
            self.photoemission.to_netcdf(folder / filename, engine="h5netcdf")

    def get_photoemission(self):
        if any(
            not hasattr(self, attr)
            for attr in ["field_amplitudes", "z_values", "dz_list"]
        ):
            self.set_field_amplitudes()

        #####
        # Here starts photoemission
        #####

        # Atomic cross-sections and assymetry parameters
        acs = self.sample.acs.to_numpy()
        asp = self.sample.asp.to_numpy()
        full_acs = np.array([acs[:, c] for c in self.layer_ids]).T
        full_asp = np.array([asp[:, c] for c in self.layer_ids]).T

        # RC flag
        rc_flag = np.zeros((self.fullsample.shape[0], self.rcs.shape[0]))
        for i, rc in self.rcs.iterrows():
            for layer_id in rc.layers:
                rc_flag[self.fullsample["id"] == layer_id, i] = 1
        rc_flag = rc_flag[:-1, :].T
        lp = rc_flag.shape[1] - 1
        binding_energies = np.array([x[0] for x in self.rcs["BE"]])

        # For a subshell Ak, this is the A_{Ak} term that is a function of the
        # assymetry parameter \eta_{Ak} and the angle \csi_{Ak} between the
        # polarization direction and the electron emission direction:
        # A_{Ak} = [1 + \eta_{Ak}(3*g/2 - 1/2)], where g = cos^2(\eta_{Ak})
        #
        #
        match self.light_polarization:
            case "p":
                gam = np.cos(np.radians(abs(self.inbetween_angle - 90))) ** 2
            case "s+p?":  # check this
                gam = np.cos(np.radians(self.inbetween_angle)) ** 2
            case "s" | _:
                gam = 0.0
        ay = np.zeros(
            (
                self.incident_angles.size,
                self.photon_energies.size,
                rc_flag.shape[0],
                self.n_of_layers - 1,
            )
        )
        nay = np.zeros(
            (
                self.incident_angles.size,
                self.photon_energies.size,
                rc_flag.shape[0],
                self.n_of_layers - 1,
            )
        )
        atom_density = (
            self.fullsample[:-1]
            .apply(
                lambda r: (
                    r.density / r.molecular_weight if r.molecular_weight > 0 else 0
                ),
                axis=1,
            )
            .values
        )
        for i, l_idx in enumerate(self.layer_indexes[1:-1]):
            term = 1.0 + (full_asp[:, [l_idx]] / 2) * (3.0 * gam - 1.0)
            for j in range(rc_flag.shape[0]):
                nay[:, :, [j], [l_idx]] = (
                    term * atom_density[l_idx] * self.rcs.loc[j, "atomN"][0]
                )
                ay[:, :, [j], [l_idx]] = (
                    term
                    * atom_density[l_idx]
                    * self.rcs.loc[j, "atomN"][0]
                    * full_acs[None, :, [l_idx]]
                )

        # Back reflection of photoelectrons
        RE = np.zeros(
            (self.incident_angles.size, self.photon_energies.size, rc_flag.shape[0])
        )
        tp = np.zeros(
            (self.incident_angles.size, self.photon_energies.size, rc_flag.shape[0])
        )
        tffag = self.incident_angles.copy()
        tffag += self.inbetween_angle
        tffag[tffag >= 90] = 180 - tffag[tffag >= 90]
        scattering_angles = np.linspace(0, 90, 9001)
        sin_sqr_scatt_angles = np.sin(np.radians(scattering_angles)) ** 2
        for ii in range(len(self.incident_angles)):
            for jj, photon_energy in enumerate(self.photon_energies):
                for m in range(rc_flag.shape[0]):
                    kinetic_energy = photon_energy - binding_energies[m]
                    if kinetic_energy <= 15.0:
                        RE[ii, jj, m] = 0.0
                        tp[jj, jj, m] = 90
                    else:
                        if abs(tffag[ii] - 90.0) < 1e-5:
                            tp[ii, jj, m] = 90
                            t1 = np.sqrt(1.0 - 15.0 / kinetic_energy)
                            t2 = (1 - t1) / (1 + t1)
                            RE[ii, jj, m] = t2**2
                        else:
                            first_test = np.argwhere(
                                sin_sqr_scatt_angles >= 15.0 / kinetic_energy
                            ).squeeze()[0]
                            values = np.degrees(
                                np.arctan(
                                    np.sqrt(
                                        sin_sqr_scatt_angles[first_test:]
                                        - 15.0 / kinetic_energy
                                    )
                                    / np.cos(np.radians(scattering_angles[first_test:]))
                                )
                            )
                            best_value = np.argwhere(tffag[ii] <= values).squeeze()[0]
                            tp[ii, jj, m] = scattering_angles[first_test + best_value]
                            t1 = np.sin(np.radians(tp[ii, jj, m])) ** 2
                            t2 = np.sqrt(1.0 - 15.0 / (kinetic_energy * t1))
                            t3 = (1.0 - t2) / (1.0 + t2)
                            RE[ii, jj, m] = t3**2

        RE = 1 - RE

        # Effective attenuation length of the photoelectrons
        # This depends on the binding energy of the subshell
        attenuation_length_by_layer = np.zeros(
            (self.photon_energies.size, rc_flag.shape[0], self.n_of_layers - 1)
        )
        attenuation_length_by_layer[:, :, 0] = 1e100
        attenuation = np.zeros(
            (
                self.incident_angles.size,
                self.photon_energies.size,
                rc_flag.shape[0],
                (self.n_of_layers - 1) * self.depth_mesh + 1,
            )
        )
        attenuation_length = np.zeros(
            (
                self.incident_angles.size,
                self.photon_energies.size,
                rc_flag.shape[0],
                (self.n_of_layers - 1) * self.depth_mesh + 1,
            )
        )
        for m in range(rc_flag.shape[0]):
            for jj, photon_energy in enumerate(self.photon_energies):
                kinetic_energy = photon_energy - binding_energies[m]
                for j, l_idx in zip(self.layer_ids[1:-1], self.layer_indexes[1:-1]):
                    attenuation_length_by_layer[jj, m, l_idx] = imfp(
                        self.minisample[self.minisample["id"].isin([j])], kinetic_energy
                    )
        h = 0
        for i, l_idx in enumerate(self.layer_indexes[:-1][::-1]):
            for j in range(self.depth_mesh + 1):
                for o in range(rc_flag.shape[0]):
                    attenuation_length[:, :, o, h] = attenuation_length_by_layer[
                        :, o, l_idx
                    ]
                    attenuation[:, :, o, h] = np.exp(
                        -self.dz_list[l_idx]
                        / (
                            attenuation_length_by_layer[:, o, l_idx]
                            * np.sin(np.radians(tp[:, :, o]))
                        )
                    )
                if j < self.depth_mesh:
                    h = h + 1

        accthick = np.zeros(self.n_of_layers)
        for i, row_data in self.fullsample.iloc[1:, :].iterrows():
            accthick[i] = accthick[i - 1] + self.fullsample.iloc[i - 1].thickness
        paccthick = accthick - self.fullsample.iloc[0].thickness

        phI = np.zeros(
            (
                self.incident_angles.size,
                self.photon_energies.size,
                rc_flag.shape[0],
                (self.n_of_layers - 1) * self.depth_mesh + 1,
            )
        )
        phimfp = np.zeros(
            (
                self.incident_angles.size,
                self.photon_energies.size,
                rc_flag.shape[0],
                (self.n_of_layers - 1) * self.depth_mesh + 1,
            )
        )
        tmpl = [0 for _ in range(rc_flag.shape[0])]
        spotsize = 0
        spotsize_correction = 1
        layer = 0
        z = 0
        k = self.z_slices
        for i in range(k + 1):
            for j in range(rc_flag.shape[0]):
                if spotsize:
                    spotsize_correction = 1 / np.sin(np.radians(tp[:, :, [j]]))

                if i == 0:
                    tmpl[j] = attenuation[:, :, [j], [k - i]]
                    phI[:, :, [j], [i]] = (
                        self.field_amplitudes[:, :, [i]]
                        * RE[:, :, [j]]
                        * ay[:, :, [j], [layer]]
                        * rc_flag[None, j, layer]
                        * spotsize_correction
                    )
                    phimfp[:, :, [j], [i]] = attenuation_length[:, :, [j], [k - i]]
                else:
                    if (
                        layer == 0
                        and self.z_values[i]
                        > paccthick[layer + 1] - self.interdiffusion[layer]
                        and layer + 1 <= lp
                        and rc_flag[j, layer + 1] != 0
                    ):
                        phI[:, :, [j], [i]] = (
                            self.field_amplitudes[:, :, [i]]
                            * RE[:, :, [j]]
                            * mix(
                                nay[:, :, [j], [layer + 1]],
                                self.interdiffusion_type[layer],
                                self.z_values[i],
                                paccthick[layer + 1],
                                self.interdiffusion[layer],
                                4,
                            )
                            * full_acs[:, [layer + 1]]
                        )
                    elif layer > 0:
                        if (
                            self.z_values[i]
                            > paccthick[layer] + self.interdiffusion[layer - 1]
                            and self.z_values[i]
                            <= paccthick[layer + 1] - self.interdiffusion[layer]
                        ):
                            phI[:, :, [j], [i]] = (
                                self.field_amplitudes[:, :, [i]]
                                * RE[:, :, [j]]
                                * ay[:, :, [j], [layer]]
                                * rc_flag[j, layer]
                            )
                        elif (
                            self.z_values[i]
                            <= paccthick[layer] + self.interdiffusion[layer - 1]
                            and self.z_values[i] > paccthick[layer]
                        ):
                            if rc_flag[j, layer] != 0:
                                phI[:, :, [j], [i]] = (
                                    self.field_amplitudes[:, :, [i]]
                                    * RE[:, :, [j]]
                                    * mix(
                                        nay[:, :, [j], [layer]],
                                        self.interdiffusion_type[layer - 1],
                                        self.z_values[i],
                                        paccthick[layer],
                                        self.interdiffusion[layer - 1],
                                        1,
                                    )
                                    * full_acs[:, [layer]]
                                )
                            elif rc_flag[j, layer] == 0 and rc_flag[j, layer - 1] != 0:
                                phI[:, :, [j], [i]] = (
                                    self.field_amplitudes[:, :, [i]]
                                    * RE[:, :, [j]]
                                    * mix(
                                        nay[:, :, [j], [layer - 1]],
                                        self.interdiffusion_type[layer - 1],
                                        self.z_values[i],
                                        paccthick[layer],
                                        self.interdiffusion[layer - 1],
                                        3,
                                    )
                                    * full_acs[:, [layer - 1]]
                                )
                        elif (
                            self.z_values[i] <= paccthick[layer + 1]
                            and self.z_values[i]
                            > paccthick[layer + 1] - self.interdiffusion[layer]
                        ):
                            if rc_flag[j, layer] != 0:
                                phI[:, :, [j], [i]] = (
                                    self.field_amplitudes[:, :, [i]]
                                    * RE[:, :, [j]]
                                    * mix(
                                        nay[:, :, [j], [layer]],
                                        self.interdiffusion_type[layer],
                                        self.z_values[i],
                                        paccthick[layer + 1],
                                        self.interdiffusion[layer],
                                        2,
                                    )
                                    * full_acs[:, [layer]]
                                )
                            elif (
                                rc_flag[j, layer] == 0
                                and layer + 1 <= lp
                                and rc_flag[j, layer + 1] != 0
                            ):
                                phI[:, :, [j], [i]] = (
                                    self.field_amplitudes[:, :, [i]]
                                    * RE[:, :, [j]]
                                    * mix(
                                        nay[:, :, [j], [layer + 1]],
                                        self.interdiffusion_type[layer],
                                        self.z_values[i],
                                        paccthick[layer + 1],
                                        self.interdiffusion[layer],
                                        4,
                                    )
                                    * full_acs[:, [layer + 1]]
                                )

                    tmpl[j] = tmpl[j] * attenuation[:, :, [j], [k - i]]
                    phI[:, :, [j], [i]] = (
                        tmpl[j] * phI[:, :, [j], [i]] * spotsize_correction
                    )
                    phimfp[:, :, [j], [i]] = attenuation_length[:, :, [j], [k - i]]

            if i < k:
                layer = int(np.fix(i / self.depth_mesh))
                z = z + self.dz_list[layer]

        self.photoemission = xr.Dataset(
            data_vars={
                row_data["label"]: (["angle", "energy", "depth"], phI[:, :, i, :])
                for i, row_data in self.rcs.iterrows()
            },
            coords={
                "angle": self.incident_angles,
                "energy": self.photon_energies,
                "depth": self.z_values,
            },
            attrs={"scan_mode": self.scan_mode},
        )
