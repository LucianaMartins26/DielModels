import cobra
import os
from tests import TEST_DIR
from diel_models.diel_models_creator import diel_models_creator


def diel_potato(model):

    diel_models_creator(model,
                        ["Sucrose[c]", "Sulfate[e]", "Nitrate[c]", "L_Histidine[c]", "L_Isoleucine[c]", "L_Leucine[c]",
                         "L_Lysine[c]", "L_Methionine[c]", "L_Phenylalanine[c]", "L_Tryptophan[c]", "L_Threonine[c]",
                         "L_Valine[c]", "L_Asparagine[c]", "L_Cystine[c]", "L_Glutamine[c]", "Glycine[c]",
                         "L_Proline[c]", "L_Tyrosine[c]", "L_Glutamate[c]", "L_Alanine[c]", "L_Aspartate[c]",
                         "L_Serine[c]", "Starch[c]", "D_Fructose[c]", "(S)_Malate[c]", "Fumarate[c]", "Citrate[c]"],
                        ["RB002"], ["RB001"], "RBS01")

    cobra.io.write_sbml_model(model, os.path.join(TEST_DIR, 'models', 'diel_potato_model.xml'))


if __name__ == '__main__':
    potato_model_path = os.path.join(TEST_DIR, 'models', 'potato_mat.xml')
    potato_model = cobra.io.read_sbml_model(potato_model_path)
    diel_potato(potato_model)
