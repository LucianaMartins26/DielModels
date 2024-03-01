import os

import cobra
import pandas as pd
from cobra.flux_analysis import pfba

from tests import TEST_DIR


def QY_AQ(non_diel_model, diel_model):
    fba_sol_nd = pfba(non_diel_model).fluxes
    fba_sol_d = pfba(diel_model).fluxes

    return fba_sol_nd, fba_sol_d


if __name__ == '__main__':
    original_model = cobra.io.read_sbml_model(os.path.join(TEST_DIR, 'models', 'Rice_Lakshmanan_fixed.xml'))
    diel_rice_L_model = cobra.io.read_sbml_model(os.path.join(TEST_DIR, 'models', "diel_rice_Lakshmanan_model.xml"))

    original_model.objective = "Straw_Biomass"
    original_model.objective_direction = "max"
    diel_rice_L_model.objective = "Biomass_Total"
    diel_rice_L_model.objective_direction = "max"

    fba_sol_non_diel, fba_sol_diel_model = QY_AQ(original_model, diel_rice_L_model)

    data_quantum_assimilation = {
        'Quantum Yield': [fba_sol_non_diel["RBPCs"] / - fba_sol_non_diel["EX_photonVis_LPAREN_e_RPAREN_"],
                          fba_sol_diel_model["RBPCs_Day"] / - fba_sol_diel_model["EX_photonVis_LPAREN_e_RPAREN__Day"]],

        'Assimilation Quotient': [fba_sol_non_diel["RBPCs"] / fba_sol_non_diel["PSIINC"],
                                  fba_sol_diel_model["RBPCs_Day"] / fba_sol_diel_model["PSIINC_Day"]]}

    tabel = pd.DataFrame(data_quantum_assimilation)

    tabel.index = ["Original Model", "Created Diel Model"]

    tabel.to_csv('QY&AQ_RiceL.csv', sep=',')

    print(tabel)
