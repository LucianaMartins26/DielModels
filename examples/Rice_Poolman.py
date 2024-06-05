import cobra
import os

from tests import TEST_DIR
from diel_models.diel_models_creator import diel_models_creator


def diel_rice_poolman(model):
    diel_models_creator(model,
                        ["SUCROSE", "SULFATE", "NITRATE", "HIS", "ILE",
                         "LEU", "LYS", "MET", "PHE", "THR", "TRP", "VAL",
                         "ARG", "CYS", "GLN", "GLY", "PRO", "TYR", "met_1117",
                         "met_1135", "ASN", "SER", "Starch_str", "FRU", "MAL",
                         "FUM", "CIT"], ["chl_Photon_tx"], nitrate_exchange_reaction=["NO3_tx"])

    cobra.io.write_sbml_model(model, os.path.join(TEST_DIR, 'models', 'diel_rice_poolman_model.xml'))


if __name__ == '__main__':
    rice_Poolman_model_path = os.path.join(TEST_DIR, 'models', 'Rice_Poolman.sbml')
    rice_Poolman_model = cobra.io.read_sbml_model(rice_Poolman_model_path)
    diel_rice_poolman(rice_Poolman_model)
