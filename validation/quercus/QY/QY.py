import os

import cobra
import pandas as pd
from cobra.flux_analysis import pfba

from tests import TEST_DIR
from validation.quercus import QUERCUS_DIR

if __name__ == '__main__':
    original_model = cobra.io.read_sbml_model(os.path.join(TEST_DIR, 'models', 'QuercusSuberGeneralModel.xml'))

    luciana_diel_model = cobra.io.read_sbml_model(os.path.join(QUERCUS_DIR, '(changed)diel_multi_quercus_model.xml'))
    emanuel_diel_model = cobra.io.read_sbml_model(os.path.join(TEST_DIR, 'models', 'Emanuel_DielMultiTissueModel.xml'))

    original_model.objective = "EX_C00205__dra"
    original_model.objective_direction = "max"
    original_model.reactions.e_Biomass_Leaf__cyto.bounds = (0.08, 0.08)
    luciana_diel_model.objective = "EX_C00205__dra_Day"
    luciana_diel_model.objective_direction = "max"
    luciana_diel_model.reactions.get_by_id("Total_biomass").bounds = (0.08, 0.08)
    emanuel_diel_model.objective = "EX_C00205__dra_Light"
    emanuel_diel_model.objective_direction = "max"
    emanuel_diel_model.reactions.Total_biomass.bounds = (0.08, 0.08)

    fba_sol_non_diel = pfba(original_model).fluxes
    fba_sol_c = pfba(luciana_diel_model).fluxes
    fba_sol_o = pfba(emanuel_diel_model).fluxes

    data_quantum_assimilation = {
        'Quantum Yield': [fba_sol_non_diel["R00024__chlo"] / - fba_sol_non_diel["EX_C00205__dra"],
                          fba_sol_c["R00024__plst_Leaf_Day"] / - fba_sol_c["EX_C00205__dra_Day"],
                          fba_sol_o["R00024__plst_Leaf_Light"] / - fba_sol_o["EX_C00205__dra_Light"]]}

    tabel = pd.DataFrame(data_quantum_assimilation)

    tabel.index = ["Original Quercus Model", "Created Diel Multi Tissue Quercus", "Original Diel Multi Tissue Quercus"]

    tabel.to_csv('QY_Diel_MultiTissue_Quercus.csv', sep=',')

    print(tabel)
