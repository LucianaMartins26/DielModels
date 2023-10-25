import cobra
import os

import pandas as pd

from tests import TEST_DIR
from diel_models.diel_models_creator import diel_models_creator


def diel_thaliana2013(model):

    diel_models_creator(model,
                        ["SUCROSE_c", "SULFATE_c", "NITRATE_c", "HIS_c", "ILE_c",
                         "LEU_c", "LYS_c", "MET_c", "PHE_c", "THR_c", "TRP_c", "VAL_c",
                         "ARG_c", "CYS_c", "GLN_c", "GLY_c", "PRO_c", "TYR_c", "met_2041",
                         "met_2074", "ASN_c", "SER_c", "STARCH_p", "FRU_c", "MAL_c",
                         "FUM_c", "CIT_c"], ["EX_x_Photon"], nitrate_exchange_reaction=["EX_x_NO3"])

    cobra.io.write_sbml_model(model, os.path.join(TEST_DIR, 'models', 'diel_thaliana2013_model.xml'))


if __name__ == '__main__':
    thaliana2013_model_path = os.path.join(TEST_DIR, 'models', 'Athaliana_cheung13.xml')
    thaliana2013_model = cobra.io.read_sbml_model(thaliana2013_model_path)
    diel_thaliana2013(thaliana2013_model)