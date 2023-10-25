import cobra
import os
from tests import TEST_DIR
from diel_models.diel_models_creator import diel_models_creator


def diel_colza(model):

    diel_models_creator(model,
                        ["sucr_a", "so4_a", "no3_a", "his_c", "ile_c",
                         "leu_c", "lys_c", "met_c", "phe_c", "thr_c", "trp_c", "val_c",
                         "arg_c", "cys_c", "gln_c", "gly_c", "pro_c", "tyr_c", "ala_c",
                         "glu_c", "asn_c", "ser_c", "starch_p", "fru_c", "mal_c",
                         "fum_c", "cit_c"], ["Ex_ph_t"], nitrate_exchange_reaction=["Ex_no3_a"], biomass_reaction_id="Biomasssynth_u")

    cobra.io.write_sbml_model(model, os.path.join(TEST_DIR, 'models', 'diel_colza_model.xml'))


if __name__ == '__main__':
    colza_model_path = os.path.join(TEST_DIR, 'models', 'Colza_bna572_plus.xml')
    colza_model = cobra.io.read_sbml_model(colza_model_path)
    diel_colza(colza_model)