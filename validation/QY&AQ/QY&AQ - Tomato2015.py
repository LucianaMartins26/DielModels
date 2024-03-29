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
    original_model = cobra.io.read_sbml_model(os.path.join(TEST_DIR, 'data', 'functional_tomato_model.xml'))
    diel_tomato_model = cobra.io.read_sbml_model(os.path.join(TEST_DIR, 'data', "diel_tomato_model.xml"))

    original_model.objective = "biomass_reaction"
    original_model.objective_direction = "max"
    diel_tomato_model.objective = "Biomass_Total"
    diel_tomato_model.objective_direction = "max"

    fba_sol_non_diel, fba_sol_diel_model = QY_AQ(original_model, diel_tomato_model)

    data_quantum_assimilation = {
        'Quantum Yield': [fba_sol_non_diel["reac_1070"] / - fba_sol_non_diel["EX_x_Photon"],
                          fba_sol_diel_model["reac_1070_Day"] / - fba_sol_diel_model["EX_x_Photon_Day"]],

        'Assimilation Quotient': [fba_sol_non_diel["reac_1070"] / fba_sol_non_diel["reac_1017"],
                                  fba_sol_diel_model["reac_1070_Day"] / fba_sol_diel_model["reac_1017_Day"]]}

    tabel = pd.DataFrame(data_quantum_assimilation)

    tabel.index = ["Original Model", "Created Diel Model"]

    tabel.to_csv('QY&AQ_Tomato15.csv', sep=',')

    print(tabel)
