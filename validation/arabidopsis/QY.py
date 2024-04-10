import os

import cobra
import pandas as pd
from cobra.flux_analysis import pfba

from tests import TEST_DIR


if __name__ == '__main__':
    original_model = cobra.io.read_sbml_model(os.path.join(TEST_DIR, 'data', 'AraGEM2010.xml'))

    diel_model = cobra.io.read_sbml_model(os.path.join(TEST_DIR, 'reconstruction_results', 'MODEL1507180028','results_troppo', 'DielModel',
                              'reconstructed_models', 'Diel_Model.xml'))

    original_model.reactions.get_by_id("BIO_L").bounds = (-1000, 1000)
    original_model.objective = "BIO_L"
    original_model.objective_direction = "max"
    diel_model.reactions.get_by_id("Biomass_Total").bounds = (-1000, 1000)
    diel_model.objective = "Biomass_Total"
    diel_model.objective_direction = "max"

    fba_sol_non_diel = pfba(original_model).fluxes
    fba_sol_diel = pfba(diel_model).fluxes

    data_quantum_assimilation = {
        'Quantum Yield': [fba_sol_non_diel["R00024_p"] / - fba_sol_non_diel["Ex16"],
                          fba_sol_diel["R00024_p_Day"] / - fba_sol_diel["Ex16_Day"]]}

    tabel = pd.DataFrame(data_quantum_assimilation)

    tabel.index = ["Original AraGEM Model", "Created Diel AraGEM"]

    tabel.to_csv('QY_Diel_AraGEM.csv', sep=',')

    print(tabel)
