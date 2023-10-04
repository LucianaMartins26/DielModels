import cobra
import os
from tests import TEST_DIR
from diel_models.diel_models_creator import diel_models_creator


def diel_medicago(model):

    diel_models_creator(model,
                        ["SUCROSE_C", "SULFATE_C", "NITRATE_C", "HIS_C", "ILE_C",
                         "LEU_C", "LYS_C", "MET_C", "PHE_C", "THR_C", "TRP_C", "VAL_C",
                         "ARG_C", "CYS_C", "GLN_C", "GLY_C", "PRO_C", "TYR_C", "L-ALPHA-ALANINE_C",
                         "L-GLUTAMATE-5-P_C", "ASN_C", "SER_C", "Starch_H", "FRUCTOSE-6P_C",
                         "MAL_C", "FUM_C", "CIT_C"], ["EX_Light_E"], "BiomassShoot",
                        ["EX_NITRATE_E"])

    cobra.io.write_sbml_model(model, os.path.join(TEST_DIR, 'models', 'diel_medicago_model.xml'))


if __name__ == '__main__':
    medicago_model_path = os.path.join(TEST_DIR, 'models', 'MedicagoTruncatula.xml')
    medicago_model = cobra.io.read_sbml_model(medicago_model_path)
    diel_medicago(medicago_model)