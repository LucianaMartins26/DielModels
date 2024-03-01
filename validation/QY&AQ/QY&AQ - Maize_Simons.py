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
    original_model = cobra.io.read_sbml_model(os.path.join(TEST_DIR, 'models', 'Maize_Simons_mat.xml'))
    diel_maize_simons_model = cobra.io.read_sbml_model(os.path.join(TEST_DIR, 'models', "diel_maize_simons_model.xml"))

    original_model.objective = "Bio_Nplus"
    original_model.objective_direction = "max"
    diel_maize_simons_model.objective = "Biomass_Total"
    diel_maize_simons_model.objective_direction = "max"

    fba_sol_non_diel, fba_sol_diel_model = QY_AQ(original_model, diel_maize_simons_model)

    data_quantum_assimilation = {
        'Quantum Yield': [fba_sol_non_diel["R00024_p"] / - fba_sol_non_diel["ExMe15"],
                          fba_sol_diel_model["R00024_p_Day"] / - fba_sol_diel_model["ExMe15_Day"]],

        'Assimilation Quotient': [fba_sol_non_diel["R00024_p"] / fba_sol_non_diel["R09503_t"],
                                  fba_sol_diel_model["R00024_p_Day"] / fba_sol_diel_model["R09503_t_Day"]]}

    tabel = pd.DataFrame(data_quantum_assimilation)

    tabel.index = ["Original Model", "Created Diel Model"]

    tabel.to_csv('QY&AQ_Maize_Simons.csv', sep=',')

    print(tabel)