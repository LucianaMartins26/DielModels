import cobra
import os
from tests import TEST_DIR
from diel_models.diel_models_creator import diel_models_creator


def diel_tomato2022(model):

    diel_models_creator(model,
                        ["sucr_v", "so4_h", "no3_v", "his_L_c", "ile_L_c",
                         "leu_L_m", "lys_L_c", "met_L_c", "phe_L_h", "thr_L_c", "trp_L_c", "val_L_c",
                         "arg_L_m", "cys_L_c", "gln_L_h", "gly_c", "pro_L_c", "tyr_L_c", "ala_D_c",
                         "glu_D_c", "asn_L_c", "ser_L_c", "starch300_h", "fru_c", "mal_L_c",
                         "fum_c", "cit_c"], ["EX_photon_h"], nitrate_exchange_reaction=["EX_no3_c"], biomass_reaction_id="BIOMASS_STEM")

    cobra.io.write_sbml_model(model, os.path.join(TEST_DIR, 'models', 'diel_tomato2022_model.xml'))


if __name__ == '__main__':
    tomato2022_model_path = os.path.join(TEST_DIR, 'models', 'tomato_Sl2183.xml')
    tomato2022_model = cobra.io.read_sbml_model(tomato2022_model_path)
    diel_tomato2022(tomato2022_model)