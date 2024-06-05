import cobra
import os

from tests import TEST_DIR
from diel_models.diel_models_creator import diel_models_creator


def diel_rice_OSI1136(model):
    diel_models_creator(model,
                        ["SUCROSE", "SULFATE", "NITRATE", "HIS", "ILE",
                         "LEU", "LYS", "MET", "PHE", "THR", "TRP", "VAL",
                         "ARG", "CYS", "GLN", "GLY", "PRO", "TYR", "met_833",
                         "met_845", "ASN", "SER", "Starch", "FRU", "MAL",
                         "FUM", "CIT"], ["chl_Photon_tx"], nitrate_exchange_reaction=["chl_NITRATE_tx"])

    cobra.io.write_sbml_model(model, os.path.join(TEST_DIR, 'models', 'diel_rice_OSI1136_model.xml'))


if __name__ == '__main__':
    rice_OSI1136_model_path = os.path.join(TEST_DIR, 'models', 'Rice_OSI1136.sbml')
    rice_OSI1136_model = cobra.io.read_sbml_model(rice_OSI1136_model_path)
    diel_rice_OSI1136(rice_OSI1136_model)
