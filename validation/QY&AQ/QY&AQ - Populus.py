import os

import cobra
import pandas as pd

from cobra.flux_analysis import pfba
from tests import TEST_DIR


def QY_AQ(non_diel_model, diel_model):
    fba_sol_non_diel = pfba(non_diel_model).fluxes
    fba_sol_diel_model = pfba(diel_model).fluxes

    return fba_sol_non_diel, fba_sol_diel_model


if __name__ == '__main__':
    original_model = cobra.io.read_sbml_model(os.path.join(TEST_DIR, 'models', 'Populus_iPop7188_fixed.xml'))
    diel_populus_model = cobra.io.read_sbml_model(os.path.join(TEST_DIR, 'models', "diel_populus_model_fixed.xml"))

    original_model.objective = "BiomassRxn"
    original_model.objective_direction = "max"
    diel_populus_model.objective = "Biomass_Total"
    diel_populus_model.objective_direction = "max"

    fba_sol_non_diel, fba_sol_diel_model = QY_AQ(original_model, diel_populus_model)

    data_quantum_assimilation = {
        'Quantum Yield': [fba_sol_non_diel["RIBULOSE_BISPHOSPHATE_CARBOXYLASE_RXN_p"] / - fba_sol_non_diel["EX_light"],
                          fba_sol_diel_model["RIBULOSE_BISPHOSPHATE_CARBOXYLASE_RXN_p_Day"] / - fba_sol_diel_model["EX_light_Day"]],

        'Assimilation Quotient': [fba_sol_non_diel["RIBULOSE_BISPHOSPHATE_CARBOXYLASE_RXN_p"] / fba_sol_non_diel["PSII_RXN"],
                                  fba_sol_diel_model["RIBULOSE_BISPHOSPHATE_CARBOXYLASE_RXN_p_Day"] / fba_sol_diel_model["PSII_RXN_Day"]]}

    tabel = pd.DataFrame(data_quantum_assimilation)

    tabel.index = ["Original Model", "Created Diel Model"]

    tabel.to_csv('QY&AQ_Populus.csv', sep=',')

    print(tabel)
