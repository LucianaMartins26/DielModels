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
    original_model = cobra.io.read_sbml_model(os.path.join(TEST_DIR, 'models', 'tomato_Sl2183.xml'))
    diel_tomato_model = cobra.io.read_sbml_model(os.path.join(TEST_DIR, 'models', "diel_tomato2022_model.xml"))

    original_model.objective = "EX_photon_h"
    original_model.objective_direction = "max"
    original_model.reactions.BIOMASS_STEM.bounds = (0.11, 0.11)
    diel_tomato_model.objective = "EX_photon_h_Day"
    diel_tomato_model.objective_direction = "max"
    diel_tomato_model.reactions.Biomass_Total.bounds = (0.11, 0.11)

    fba_sol_non_diel, fba_sol_diel_model = QY_AQ(original_model, diel_tomato_model)

    data_quantum_assimilation = {
        'Quantum Yield': [fba_sol_non_diel["RBPCh"] / - fba_sol_non_diel["EX_photon_h"],
                          fba_sol_diel_model["RBPCh_Day"] / - fba_sol_diel_model["EX_photon_h_Day"]],

        'Assimilation Quotient': [fba_sol_non_diel["RBPCh"] / fba_sol_non_diel["PSII_h"],
                                  fba_sol_diel_model["RBPCh_Day"] / fba_sol_diel_model["PSII_h_Day"]]}

    tabel = pd.DataFrame(data_quantum_assimilation)

    tabel.index = ["Original Model", "Created Diel Model"]

    tabel.to_csv('QY&AQ_Tomato22.csv', sep=',')

    print(tabel)
