import cobra
import os
from tests import TEST_DIR
from diel_models.diel_models_creator import diel_models_creator


def diel_quercus(model):

    diel_models_creator(model,
                        ["C00089__cyto", "C00059__cyto", "C00244__cyto", "C00135__cyto", "C00407__cyto", "C00123__cyto",
                         "C00047__cyto", "C00073__cyto", "C02265__cyto", "C00188__cyto", "C00525__cyto", "C00183__cyto",
                         "C00062__cyto", "C00491__cyto", "C00064__cyto", "C00037__cyto", "C00148__cyto", "C00082__cyto",
                         "C01401__cyto", "C00025__cyto", "C00152__cyto", "C00065__cyto", "C00369__cyto", "C02336__cyto",
                         "C00208__cyto", "C00122__cyto", "C00158__cyto"], ["EX_C00205__dra"], "e_Biomass_Leaf__cyto",
                        ["EX_C00244__dra"])

    cobra.io.write_sbml_model(model, os.path.join(TEST_DIR, 'models', 'diel_quercus_model.xml'))


if __name__ == '__main__':
    quercus_model_path = os.path.join(TEST_DIR, 'models', 'QuercusSuberGeneralModel.xml')
    quercus_model = cobra.io.read_sbml_model(quercus_model_path)
    diel_quercus(quercus_model)