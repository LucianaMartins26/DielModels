import cobra
import os
from tests import TEST_DIR
from diel_models.diel_models_creator import diel_models_creator


def diel_rice(model):
    inactive = [
        "RBPC2s",
        "Coleoptile_Biomass",
        "PRISM_blue_LED",
        "PRISM_red_LED",
        "PRISM_white_LED",
        "PRISM_green_LED",
        "GDHym",
        "GDHm",
        "AGATx",
        "AGATs",
        "ICDHc",
        "GTHPs",
        "GLCNGBc",
        "GLCNGAc",
        "MDHs",
        "MDHc",
        "ASPTAm",
        "PDHam1m",
        "PDHam2m",
        "PDHe2m",
        "PDHe3m",
        "THR3DHx",
        "FDHNc",
        "SULOm",
        "ASNS1c",
        "GLYCORc",
        "TYRTAs",
        "ARGOAT1s",
        "PGI2c",
        "PGI2s",
        "GAMPTc",
        "FTHFLc",
        "CALANc",
        "FORAc",
        "SHMTs",
        "MLTHFRs",
        "METSc",
        "GAPDHys",
        "GAPDH2s",
        "MTHFDm",
        "MTHFDc",
        "FTHFCLc",
        "MTHFDym",
        "MTHFDys",
        "GLYK2s",
        "UREASEc",
        "ATSc",
        "SHSL1s",
        "SPPAs",
        "PFPc",
        "PTOXs",
        "PFKc",
        "PFKs",
        "AAs",
        "HCO3Es",
        "HCO3Em",
        "CHLASEs",
        "ALTNDAc",
        "NADOR2u",
        "AKGCITtm",
        "AKGICITtm",
        "MALICITtm",
        "MALOAAtm",
        "OAAAKGtm",
        "OAACITtm",
        "OAAICITtm",
        "5FTHFtm",
        "MLTHFtm",
        "NA1Htm",
        "PInatm",
        "5FTHFts",
        "5MTHFts",
        "G3P_LPAREN_pi_RPAREN_tsr",
        "G6PA_LPAREN_pi_RPAREN_ts",
        "G6PB_LPAREN_pi_RPAREN_ts",
        "PEPPIts",
        "PINA1ts",
        "IPADNEts",
        "TZTNts",
        "FA140CoAr",
        "FA160CoAr",
        "FA161CoAr",
        "FA180CoAr",
        "FA181CoAr",
        "FA183CoAr"
    ]
    for i in inactive:
        model.reactions.get_by_id(i).bounds = (0, 0)

    for reaction in model.reactions:
        if (reaction.id.startswith("EX_") and "C" in reaction.reactants[0].formula
                and reaction.id != "EX_co2_LPAREN_e_RPAREN_"):
            print(reaction.id)
            reaction.bounds = (0, 1000)

    cobra.io.write_sbml_model(model, os.path.join(TEST_DIR, 'models', 'Rice_Lakshmanan_fixed.xml'))

    diel_models_creator(model,
                        ["sucr_c", "so4_c", "no3_c", "his_DASH_L_c", "ile_DASH_L_c", "leu_DASH_L_c", "lys_DASH_L_c",
                         "met_DASH_L_c", "phe_DASH_L_c", "thr_DASH_L_c", "trp_DASH_L_c", "val_DASH_L_c", "arg_DASH_L_c",
                         "cys_DASH_L_c", "glu_DASH_L_c", "gly_c", "pro_DASH_L_c", "tyr_DASH_L_c", "ala_DASH_L_c",
                         "gln_DASH_L_c", "asn_DASH_L_c", "ser_DASH_L_c", "starch_s", "fru_DASH_B_c", "mal_DASH_L_c",
                         "fum_c", "cit_c"], ["EX_photonVis_LPAREN_e_RPAREN_"], ["EX_no3_LPAREN_e_RPAREN_"],
                        "Straw_Biomass")

    cobra.io.write_sbml_model(model, os.path.join(TEST_DIR, 'models', 'diel_rice_Lakshmanan_model.xml'))


if __name__ == '__main__':
    rice_model_path = os.path.join(TEST_DIR, 'models', 'Rice_Lakshmanan.xml')
    rice_model = cobra.io.read_sbml_model(rice_model_path)
    diel_rice(rice_model)
