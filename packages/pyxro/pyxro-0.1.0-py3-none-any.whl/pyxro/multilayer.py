import json
from copy import deepcopy
from typing import Any, Dict, Literal, Optional, TypedDict

import numpy as np
import pandas as pd
from periodictable import formula as pt_formula
from periodictable.xsf import index_of_refraction as xsf_iof

from pyxro.defaults import ATOM_INFO, DEFAULT_INPUT, DEFAULT_LAYER, FORMULA_DATA


def expand_layers(
    layers,
    vacuum: Optional[float] = None,
    interdiffusion: Optional[Dict[str, Any]] = None,
) -> pd.DataFrame:
    """
    Expands a list of layers to create additional copies of each layer as specified by its `repeat` attribute,
    and adds interdiffusion length between adjacent layers, if specified. Returns the modified layers as a pandas DataFrame.

    Args:
        layers (list): A list of dictionaries representing each layer.
        vacuum (float, optional): The thickness of a vacuum layer to add to the start of the layer stack.
        interdiffusion (list, optional): A list of dictionaries containing interdiffusion lengths between adjacent layers.

    Returns:
        pandas.DataFrame: A DataFrame containing the modified layers.

    """

    # Create a vacuum layer if specified, else start with an empty list.
    if vacuum is not None and vacuum > 0:
        output_layers = [DEFAULT_LAYER.copy()]
        output_layers[0].update(
            {
                "id": 0,
                "name": "Vacuum",
                "formula": "",
                "thickness": vacuum,
            }
        )
    else:
        output_layers = []

    # Keep track of processed indices to avoid duplicate layers.
    processed_indices = set()

    for index, layer in enumerate(layers):
        if index in processed_indices:
            continue

        if layer["repeat"] > 1:
            # Create a list of multiple copies of the current layer.
            multiple_layers = [layer.copy()]
            processed_indices.add(index)

            # Find all subsequent layers with the same repeat and add to the list.
            for lid in range(index + 1, len(layers)):
                if layers[lid]["repeat"] == layer["repeat"]:
                    multiple_layers.append(layers[lid].copy())
                    processed_indices.add(lid)

            # Create and append the specified number of copies of each layer to the output_layers list.
            for rep in range(layer["repeat"]):
                for index, layer in enumerate(multiple_layers):
                    layer_name = f"{layer['name']}_{rep+1}"
                    layer = layer.copy()
                    layer["name"] = layer_name
                    output_layers.append(layer.copy())
        else:
            output_layers.append(layer.copy())
            processed_indices.add(index)

    # If interdiffusion is specified, add interdiffusion lengths between adjacent layers.
    if interdiffusion is not None:
        interdiffusion_list = {}
        for row in interdiffusion:
            a, b = [int(x) for x in row["interface"].split("_")]
            interdiffusion_list[(a, b)] = [row["type"], row["length"]]

        for l_curr, l_next in zip(output_layers, output_layers[1:]):
            if (l_curr["id"], l_next["id"]) in interdiffusion_list:
                l_curr["interdiffusion"] = interdiffusion_list[
                    (l_curr["id"], l_next["id"])
                ][1]
                l_curr["interdiffusion_type"] = interdiffusion_list[
                    (l_curr["id"], l_next["id"])
                ][0]
            else:
                l_curr["interdiffusion"] = 0.0
                l_curr["interdiffusion_type"] = "none"

    return pd.DataFrame(output_layers)


def create_axis(axis_range):
    return np.linspace(
        axis_range["min"],
        axis_range["max"],
        int((axis_range["max"] - axis_range["min"]) / axis_range["step"]) + 1,
    )


class Layer(TypedDict, total=False):
    id: int
    name: str
    formula: str
    density: float
    repeat: int
    thickness: float
    molecular_weight: float
    num_valence_electrons: int
    energy_gap: float


class MultilayerSample(object):
    def __init__(self, name: str = "Sample", filename: str = "sample.yxro"):
        self.input = deepcopy(DEFAULT_INPUT)
        self.input["name"] = name
        self.input["layers"] = []
        self.filename = filename

    def add_layer(
        self,
        where: int = -1,
        template: Optional[str] = None,
        layer: Optional[Layer] = None,
    ) -> None:
        """Adds a new layer to the input structure.

        Args:
            where: The index at which to insert the new layer. If negative, the layer
                will be appended to the end.
            template: The name of a template layer to use as a starting point.
            layer: A dictionary of layer properties.

        Returns:
            None.
        """
        new_layer = DEFAULT_LAYER.copy()

        if template is not None:
            if template in FORMULA_DATA["name"].values:
                new_layer.update(
                    FORMULA_DATA[FORMULA_DATA["name"] == template].to_dict("records")[0]
                )
            else:
                print(f"Template '{template}' was not found. Aborting")
                return

        if layer is not None:
            new_layer.update(layer)

        formula = pt_formula(new_layer["formula"])
        molecular_weight = formula.mass
        num_valence_electrons = sum(
            v * ATOM_INFO[str(k)]["nvalence"] for k, v in formula.atoms.items()
        )
        new_layer.update(
            {
                "molecular_weight": molecular_weight,
                "num_valence_electrons": num_valence_electrons,
            }
        )

        if where < 0:
            self.input["layers"].append(new_layer)
        else:
            self.input["layers"].insert(where, new_layer)

        for i, _ in enumerate(self.input["layers"]):
            self.input["layers"][i]["id"] = i + 1

    def set_scan_mode(
        self, scan_mode: Literal["incident_angle", "photon_energy", "two_axis"]
    ) -> None:
        self.scan_mode = scan_mode

    def set_axis(self, axis=None, range=None, fixed_value=None):
        if not axis:
            return

        axis_dict = {
            axis: {
                "min": 0,
                "step": 0,
                "max": 0,
                "fixed_value": 0.0,
            }
        }

        if range:
            min_value, step_value, max_value = range
            axis_dict[axis].update(
                {"min": min_value, "step": step_value, "max": max_value}
            )

        if fixed_value:
            axis_dict[axis].update({"fixed_value": fixed_value})

        self.input["axes"].update(axis_dict)

    def load_sample(self, filename: Optional[str] = None) -> None:
        """Loads a sample from a YAML file.

        Args:
            filename: The path to the YAML file. If not specified, the default
                filename will be used.

        Returns:
            None.
        """
        if filename is None:
            filename = self.filename

        with open(filename, "r") as fp:
            self.input.update(json.load(fp))

    def save_sample(self, filename: Optional[str] = None) -> None:
        """Saves a sample to a YAML file.

        Args:
            filename: The path to the YAML file. If not specified, the default
                filename will be used.

        Returns:
            None.
        """
        if filename is None:
            filename = self.filename

        with open(filename, "w") as fp:
            json.dump(self.input, fp)

    def get_energy_axis(self):
        """
        Get the energy axis based on the input setup parameters.

        Returns:
            numpy.ndarray: Energy axis values.
        """
        match self.input["setup"]["scan_mode"]:
            case "photon_energy" | "two_axis":
                return create_axis(self.input["axes"]["photon_energy"])
            case "incident_angle":
                return np.array([self.input["axes"]["photon_energy"]["fixed_value"]])

    def get_angle_axis(self):
        """
        Get the incident angle axis based on the input setup parameters.

        Returns:
            numpy.ndarray: Incident angle axis values.
        """
        match self.input["setup"]["scan_mode"]:
            case "incident_angle" | "two_axis":
                return create_axis(self.input["axes"]["incident_angle"])
            case "photon_energy":
                return np.array([self.input["axes"]["incident_angle"]["fixed_value"]])

    def get_depth_axis(self):
        """
        Get the depth axis based on the input setup parameters.

        Returns:
            numpy.ndarray: Depth axis values.
        """
        return create_axis(self.input["axes"]["depth"])

    def get_sample(self):
        return pd.DataFrame(self.input["layers"])

    def get_fullsample(self):
        return expand_layers(
            self.input["layers"],
            vacuum=self.input["setup"]["vacuum_layer"],
            interdiffusion=self.input["interdiffusion"],
        )

    def set_other_info(self) -> None:
        """
        Set additional information for each layer in the input dictionary.
        The function adds the molecular weight and valence electrons information
        for each layer by parsing the formula string.

        Args:
            self (object): The class object.
        """
        layers = self.input["layers"]

        # Check for NaN formula strings. This can happen if the formula is not
        # specified in the input file.
        for layer in layers:
            if layer["formula"] != "NaN":
                formula = pt_formula(layer["formula"])

                # Update the molecular weight and valence electrons fields.
                layer.update(
                    {
                        "molecular_weight": formula.mass,
                        "num_valence_electrons": sum(
                            v * ATOM_INFO[str(k)]["nvalence"]
                            for k, v in formula.atoms.items()
                        ),
                    }
                )

        self.input["layers"] = layers

    # def calculate_reflectivity(self, progress=None):
    #     self.Reflectivity = calculate.reflectivity(self, progress=progress)
    #     return self.Reflectivity

    # def calculate_electric_field(self, progress=None):
    #     self.ElectricField = calculate.electric_field(self, progress=progress)
    #     return self.ElectricField

    # def export_reflectivity(self, filename="reflectivity.nc"):
    #     if self.Reflectivity is not None:
    #         self.Reflectivity.to_netcdf(filename, engine="h5netcdf")

    # def export_electric_field(self, filename="electric_field.nc"):
    #     if self.ElectricField is not None:
    #         self.ElectricField.to_netcdf(filename, engine="h5netcdf")

    def calculate_optical_constants(self):
        energy_range = self.get_energy_axis()
        layers = pd.DataFrame(self.input["layers"])
        self.opc = pd.DataFrame({"E": energy_range}).set_index("E")
        self.opc[0] = 0
        for i, v in layers[["id", "formula", "density"]].iterrows():
            if v.formula != "NaN":  # add other tests
                self.opc[v.id] = 1 - xsf_iof(
                    v.formula, density=float(v.density), energy=energy_range / 1000
                )

    def export_optical_constants(self, setlayers=False):
        layers = pd.DataFrame(self.input["layers"]).set_index("id")
        for layer_id in self.opc.columns.unique(level=0):
            if layer_id == 0:
                continue
            fname = "generated_{}.opc".format(layers.loc[layer_id]["formula"])
            self.opc.loc[:, layer_id].to_csv(fname, sep=" ", header=None)

            if setlayers:
                self.input["layers"][layer_id]["opcfile"] = fname

    # def load_acs_values(self, acsdir = None):
    #     if acsdir is None:
    #         acsdir = os.path.join(self.folder, self.input['folders']['ACS'])

    #     energy_range = self.get_energy_axis()

    #     rocking_curves = pd.DataFrame(self.input['rocking_curves'])
    #     self.acs = pd.DataFrame({'E': energy_range}).set_index('E')
    #     self.acs[0] = 0
    #     self.asp = pd.DataFrame({'E': energy_range}).set_index('E')
    #     self.asp[0] = 0

    #     # This should have three indexes: energy,layer,rocking_curve
    #     # to accomodate multiple rocking_curves per layer. Right now
    #     # it is working just like yxro (not good): order of rocking
    #     # curves has to be in the order of the layers
    #     for _, layer in pd.DataFrame(self.input['layers']).iterrows():
    #         self.acs[layer.id] = 0
    #         self.asp[layer.id] = 0
    #         for _, rc in rocking_curves.iterrows():
    #             if layer.id in rc.layers:
    #                 fname = os.path.join(acsdir, rc.acsfile)
    #                 fdata = pd.read_csv(fname, delimiter='\t', header=None)

    #                 acs_interp = interp1d(fdata.iloc[:, 0], fdata.iloc[:, 1])
    #                 asp_interp = interp1d(fdata.iloc[:, 0], fdata.iloc[:, 4])

    #                 self.acs[layer.id] = acs_interp(energy_range)
    #                 self.asp[layer.id] = asp_interp(energy_range)

    # def export_ACS_files(self, setlayers = False, acsdir = None):
    #     if acsdir is None:
    #         acsdir = os.path.join(self.folder, self.input['folders']['ACS'])

    #     if not os.path.isdir(acsdir):
    #         os.mkdir(acsdir)

    #     for i, v in self.rocking_curves[['id', 'orbital']].iterrows():
    #         orbital = str(v.orbital).replace(' ', '')
    #         out_fname = 'rc{}_{}.acs'.format(v.id, orbital)
    #         out_fpath = os.path.join(acsdir, out_fname)

    #         in_fname = pkg_resources.resource_filename('swhub', "data/acs/{}.txt".format(orbital))
    #         dt = pd.read_csv(in_fname, header = None, delimiter = '\s+', names = ['E', 'x', 'y', 'z'])
    #         dt['assym_x'] = 2
    #         dt['assym_y'] = 2
    #         dt['assym_z'] = 2
    #         dt.to_csv(out_fpath, sep = '\t', header = None, index = False)

    #         if setlayers:
    #             self.input['rocking_curves'][i]['acs'] = out_fname

    #     if setlayers:
    #         self.rocking_curves = pd.DataFrame(self.input['rocking_curves'])
