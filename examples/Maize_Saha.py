import cobra
import os
from tests import TEST_DIR
from diel_models.diel_models_creator import diel_models_creator

def diel_maize_saha(model):

    diel_models_creator(model,
                        ['C00089_c', 'C00059_c', 'C00244_c', 'C00135_c', 'C00407_c', 'C00123_c', 'C00047_c', 'C00073_c',
                         'C00079_c', 'C00078_c', 'C00188_c', 'C00183_c', 'C00152_c', 'C00491_c', 'C00025_c', 'C00037_c',
                         'C00148_c', 'C00082_c', 'C00064_c', 'C00041_c', 'C00049_c', 'C00065_c', 'C00369_p', 'C00095_c',
                         'C00149_c', 'C00122_c', 'C00158_c'], ["EX_hv"], ["EX_C00244"], "Biomass_synthesis")

    cobra.io.write_sbml_model(model, os.path.join(TEST_DIR, 'models', 'diel_maize_saha_model.xml'))


if __name__ == '__main__':
    maize_saha_model_path = os.path.join(TEST_DIR, 'models', 'Maize_Saha2011_v2.xml')
    maize_saha_model = cobra.io.read_sbml_model(maize_saha_model_path)
    diel_maize_saha(maize_saha_model)