import cobra
import os
from tests import TEST_DIR
from diel_models.diel_models_creator import diel_models_creator


def diel_populus(model):

    diel_models_creator(model,
                        ["sucrose_c", "sulfate_c", "nitrate_c", "his_p", "ile_c",
                         "leu_c", "lys_c", "met_c", "phe_c", "thr_c", "trp_c", "val_c",
                         "arg_c", "cys_c", "gln_c", "gly_c", "pro_c", "tyr_c", "d_alanine_p",
                         "glt_c", "asn_c", "ser_c", "starch_p", "beta_d_fructose_c", "mal_c",
                         "fum_c", "cit_c"], ["EX_light"], nitrate_exchange_reaction=["EX_nitrate"], biomass_reaction_id="BiomassRxn")

    cobra.io.write_sbml_model(model, os.path.join(TEST_DIR, 'models', 'diel_populus_model_fixed.xml'))


if __name__ == '__main__':
    populus_model_path = os.path.join(TEST_DIR, 'models', 'Populus_iPop7188_fixed.xml')
    populus_model = cobra.io.read_sbml_model(populus_model_path)
    diel_populus(populus_model)