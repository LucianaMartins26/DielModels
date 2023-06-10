import os
import cobra
from tests import TEST_DIR
from diel_models.diel_models_creator import diel_models_creator


def diel_model(model):
    diel_models_creator(model,
                        ["SUCROSE_Cyto", "SULFATE_Cyto", "NITRATE_Cyto", "HIS_Cyto", "ILE_Cyto", "LEU_Cyto", "LYS_Cyto",
                         "MET_Cyto", "PHE_Cyto", "THR_Cyto", "TRP_Cyto", "VAL_Cyto", "ARG_Cyto", "CYS_Cyto", "GLN_Cyto",
                         "x_GLT", "GLY_Cyto", "TYR_Cyto", "x_ALA", "ASN_Cyto", "SER_Cyto", "x_ASPARTATE", "STARCH_Cyto",
                         "FRU_Cyto", "MAL_Cyto", "FUM_Cyto", "CIT_Cyto"], 'EX_x_Photon', 'biomass_reaction', 'EX_x_NO3')

    cobra.io.write_sbml_model(model, os.path.join(TEST_DIR, 'data', 'diel_tomato_model.xml'))


if __name__ == '__main__':
    tomato_model_path = os.path.join(TEST_DIR, 'data', 'functional_tomato_model.xml')
    tomato_model = cobra.io.read_sbml_model(tomato_model_path)
    diel_model(tomato_model)
