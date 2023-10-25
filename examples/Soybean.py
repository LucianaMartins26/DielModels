import cobra
import os
from tests import TEST_DIR
from diel_models.diel_models_creator import diel_models_creator


def diel_soybean(model):

    diel_models_creator(model,
                        ["SUCROSE_c", "SULFATE_c", "NITRATE_c", "HIS_c", "ILE_c",
                         "LEU_c", "LYS_c", "MET_c", "PHE_c", "THR_c", "TRP_c", "VAL_c",
                         "ARG_c", "CYS_c", "GLN_c", "GLY_c", "PRO_c", "TYR_c", "D-ALANINE_c",
                         "D-GLT_c", "ASN_c", "SER_c", "STARCH_p", "FRU_c", "MAL_c",
                         "FUM_c", "CIT_c"], ["Photon_tx"], nitrate_exchange_reaction=["NO3_tx"])

    cobra.io.write_sbml_model(model, os.path.join(TEST_DIR, 'models', 'diel_soybean_model.xml'))


if __name__ == '__main__':
    soybean_model_path = os.path.join(TEST_DIR, 'models', 'Soybean_GSMM.xml')
    soybean_model = cobra.io.read_sbml_model(soybean_model_path)
    met_list = ["SUCROSE_c", "SULFATE_c", "NITRATE_c", "HIS_c", "ILE_c",
                         "LEU_c", "LYS_c", "MET_c", "PHE_c", "THR_c", "TRP_c", "VAL_c",
                         "ARG_c", "CYS_c", "GLN_c", "GLY_c", "PRO_c", "TYR_c", "D-ALANINE_c",
                         "D-GLT_c", "ASN_c", "SER_c", "STARCH_p", "FRU_c", "MAL_c",
                         "FUM_c", "CIT_c"]
    for metabolite in met_list:
        if not soybean_model.metabolites.get_by_id(metabolite).name:
            soybean_model.metabolites.get_by_id(metabolite).name = metabolite.replace("_c", "").replace("_p", "").lower()
    diel_soybean(soybean_model)