import os

import cobra
import pandas as pd
from cobra.flux_analysis import pfba

from tests import TEST_DIR

if __name__ == '__main__':
    original_model = cobra.io.read_sbml_model(os.path.join(TEST_DIR, 'models', 'QuercusSuberGeneralModel.xml'))

    luciana_diel_model = cobra.io.read_sbml_model("quercus/(changed)diel_multi_quercus_model.xml")
    emanuel_diel_model = cobra.io.read_sbml_model(os.path.join(TEST_DIR, 'models', 'Emanuel_DielMultiTissueModel.xml'))

    fba_sol_non_diel = pfba(original_model).fluxes
    fba_sol_c = pfba(luciana_diel_model).fluxes
    fba_sol_o = pfba(emanuel_diel_model).fluxes

    data_quantum_assimilation = {
        'Quantum Yield': [fba_sol_non_diel["R00024__chlo"] / - fba_sol_non_diel["EX_C00205__dra"],
                          fba_sol_c["R00024__plst_Leaf_Day"] / - fba_sol_c["EX_C00205__dra_Day"],
                          fba_sol_o["R00024__plst_Leaf_Light"] / - fba_sol_o["EX_C00205__dra_Light"]],

        'Assimilation Quotient': [fba_sol_non_diel["R00024__chlo"] / - fba_sol_non_diel["Photosystem_II__chlo"],
                                  fba_sol_c["R00024__plst_Leaf_Day"] / fba_sol_c["Photosystem_II__plst_Leaf_Day"],
                                  fba_sol_o["R00024__plst_Leaf_Light"] / fba_sol_o["Photosystem_II__plst_Leaf_Light"]]}

    tabel2 = pd.DataFrame(data_quantum_assimilation)

    tabel2.index = ["Original Quercus Model", "Created Diel Multi Tissue Quercus", "Original Diel Multi Tissue Quercus"]

    tabel2.to_csv('QY&AQ_Diel_MultiTissue_Quercus.csv', sep=',')

    print(tabel2)
