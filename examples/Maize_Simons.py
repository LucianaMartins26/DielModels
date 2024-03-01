import cobra
import os
from tests import TEST_DIR
from diel_models.diel_models_creator import diel_models_creator


def diel_maize_simons(model):
    diel_models_creator(model,
                        ['C00059[c]', 'C00059[d]', 'C00244[c]', 'C00244[d]',
                         'C00095[c]', 'C00095[d]', 'C00099[d]',
                         'C00099[c]', 'C00064[c]', 'C00064[d]', 'C00089[c]',
                         'C00089[d]', 'C00122[c]', 'C00122[d]', 'C00135[c]', 'C00135[d]', 'C00407[c]', 'C00407[d]',
                         'C00123[c]', 'C00123[d]', 'C00047[c]', 'C00047[d]',
                         'C00073[c]', 'C00073[d]', 'C00079[c]', 'C00079[d]', 'C00188[c]', 'C00188[d]', 'C00037[c]',
                         'C00037[d]',
                         'C00183[c]', 'C00183[d]', 'C00062[c]', 'C00062[d]', 'C00491[c]', 'C00491[d]', 'C00148[c]',
                         'C00148[d]',
                         'C00082[c]', 'C00082[d]', 'C00025[c]', 'C00025[d]', 'C00152[c]', 'C00152[d]', 'C00065[c]',
                         'C00065[d]',
                         'C00369[c]', 'C00369[d]', 'C00149[c]', 'C00149[d]', 'C00158[c]', 'C00158[d]'],
                        ["ExMe15", "ExBe15"],
                        ["ExBe10"], "Bio_Nplus",
                        tissues=["Bundle Sheath", "Mesophyll"])

    cobra.io.write_sbml_model(model, os.path.join(TEST_DIR, 'models', 'diel_maize_simons_model.xml'))


if __name__ == '__main__':
    maize_simons_model_path = os.path.join(TEST_DIR, 'models', 'Maize_Simons_mat.xml')
    maize_simons_model = cobra.io.read_sbml_model(maize_simons_model_path)
    diel_maize_simons(maize_simons_model)
