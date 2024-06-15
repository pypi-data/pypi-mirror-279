import json
from importlib.resources import as_file, files

from pandas import read_csv

DEFAULT_LAYER = {
    "id": 0,
    "name": "Si",
    "formula": "Si",
    "density": 0.0,
    "repeat": 1,
    "thickness": 0.0,
    "molecular_weight": 0.0,
    "num_valence_electrons": 0,
    "energy_gap": 0.0,
}

with as_file(files("pyxro.data").joinpath("atominfo.json")) as f:
    with open(f, "r") as fp:
        ATOM_INFO = json.load(fp)

with as_file(files("pyxro.data").joinpath("binding_energies.csv")) as f:
    BINDING_ENERGIES_LIST = read_csv(f, index_col=0)

with as_file(files("pyxro.data").joinpath("corelevel_data.csv")) as f:
    CORELEVEL_DATA = read_csv(f, index_col=["atom", "level"])

with as_file(files("pyxro.data").joinpath("formula_data.csv")) as f:
    FORMULA_DATA = read_csv(f)

DEFAULT_ROCKING_CURVE = {
    "id": 0,
    "label": "",
    "orbital": "",
    "atomZ": 0,
    "layers": [],
    "imfp": [],
    "atomN": [],
}

LAYER_COLUMN_NAMES = list(DEFAULT_LAYER.keys())

DEFAULT_INPUT = {
    "name": "",
    "setup": {
        "scan_mode": "incident_angle",
        "light_polarization": "p",
        "integral_mesh": 40,
        "inbetween_angle": 90,
        "vacuum_layer": 100.0,
    },
    "axes": {
        "incident_angle": {
            "min": 0.0,
            "step": 0.5,
            "max": 20.0,
            "fixed_value": 0.0,
        },
        "photon_energy": {
            "min": 0.0,
            "step": 0.0,
            "max": 0.0,
            "fixed_value": 900.0,
        },
        "depth": {
            "min": 0.0,
            "step": 0.0,
            "max": 0.0,
            "fixed_value": 0.0,
        },
    },
    "layers": [],
    "interdiffusion": [],
    "rocking_curves": [],
}
