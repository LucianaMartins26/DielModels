import cobra
import os
from tests import TEST_DIR
from diel_models.diel_models_creator import diel_models_creator


def diel_maize_iEB5204(model):

    diel_models_creator(model,
                        ["SUCROSE", "SULFATE", "NITRATE", "HIS", "ILE", "LEU", "LYS", "MET", "PHE", "TRP", "THR", "VAL",
                         "ASN", "CYS", "GLN", "GLY", "PRO", "TYR", "GLT", "L_alanine", "L_ASPARTATE", "SER",
                         "starch_monomer_equivalent", "BETA_D_FRUCTOSE", "MAL", "FUM", "CIT"], ["tx__Light_"],
                        ["tx_NITRATE"])

    cobra.io.write_sbml_model(model, os.path.join(TEST_DIR, 'models', 'diel_maizeiEB5204_model.xml'))


if __name__ == '__main__':
    maizeiEB5204_model_path = os.path.join(TEST_DIR, 'models', 'Maize_iEB5204.xml')
    maizeiEB5204_model = cobra.io.read_sbml_model(maizeiEB5204_model_path)
    diel_maize_iEB5204(maizeiEB5204_model)
