import cobra
import os
from tests import TEST_DIR
from diel_models.diel_models_creator import diel_models_creator


def diel_rice(model):

    diel_models_creator(model,
                        ["sucr_c", "so4_c", "no3_c", "his_DASH_L_c", "ile_DASH_L_c", "leu_DASH_L_c", "lys_DASH_L_c",
                         "met_DASH_L_c", "phe_DASH_L_c", "thr_DASH_L_c", "trp_DASH_L_c", "val_DASH_L_c", "arg_DASH_L_c",
                         "cys_DASH_L_c", "glu_DASH_L_c", "gly_c", "pro_DASH_L_c", "tyr_DASH_L_c", "ala_DASH_L_c",
                         "gln_DASH_L_c", "asn_DASH_L_c", "ser_DASH_L_c", "starch_s", "fru_DASH_B_c", "mal_DASH_L_c",
                         "fum_c", "cit_c"], ["EX_photonVis_LPAREN_e_RPAREN_"], "Straw_Biomass",
                        ["EX_no3_LPAREN_e_RPAREN_"])

    cobra.io.write_sbml_model(model, os.path.join(TEST_DIR, 'models', 'diel_rice_Lakshmanan_model.xml'))


if __name__ == '__main__':
    rice_model_path = os.path.join(TEST_DIR, 'models', 'Rice_Lakshmanan.xml')
    rice_model = cobra.io.read_sbml_model(rice_model_path)
    diel_rice(rice_model)