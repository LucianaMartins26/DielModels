import os

import cobra
import pandas as pd
from cobra.flux_analysis import pfba

from tests import TEST_DIR

def QY(non_diel_model, diel_model):
    fba_sol_non_diel = pfba(non_diel_model).fluxes
    fba_sol_diel_model = pfba(diel_model).fluxes

    return fba_sol_non_diel, fba_sol_diel_model


if __name__ == '__main__':
    original_model = cobra.io.read_sbml_model(os.path.join(TEST_DIR, 'data', 'AraGEM2010.xml'))

    diel_model = cobra.io.read_sbml_model(os.path.join(TEST_DIR, 'reconstruction_results', 'MODEL1507180028','results_troppo', 'DielModel',
                              'reconstructed_models', 'Diel_Model.xml'))

    original_model.objective = "Ex16"
    original_model.objective_direction = "max"
    original_model.reactions.BIO_L.bounds = (0.11, 0.11)
    diel_model.objective = "Ex16_Day"
    diel_model.objective_direction = "max"
    diel_model.reactions.Biomass_Total.bounds = (0.11, 0.11)

    fba_sol_non_diel, fba_sol_diel_model = QY(original_model, diel_model)

    data_quantum_assimilation = {
        'Quantum Yield': [fba_sol_non_diel["R00024_p"] / - fba_sol_non_diel["Ex16"],
                          fba_sol_diel_model["R00024_p_Day"] / - fba_sol_diel_model["Ex16_Day"]]}

    tabel = pd.DataFrame(data_quantum_assimilation)

    tabel.index = ["Original AraGEM Model", "Created Diel AraGEM"]

    tabel.to_csv('QY_AraGEM.csv', sep=',')

    print(tabel)
