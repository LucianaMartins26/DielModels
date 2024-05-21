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

    original_model.objective = "EX_x_Photon"
    original_model.objective_direction = "max"
    diel_tomato_model.objective = "EX_x_Photon_Day"
    diel_tomato_model.objective_direction = "max"
    original_model.reactions.biomass_reaction.bounds = (0.11, 0.11)
    diel_tomato_model.reactions.Biomass_Total.bounds = (0.11, 0.11)

    media = ["EX_x_CO2", "EX_x_Ca", "EX_x_Fe", "EX_x_K", "EX_x_Mg", "EX_x_NO3", "EX_x_NH4", "EX_x_O2", "EX_x_Photon",
             "EX_x_SO4", "EX_x_Zn", "EX_x_Pi"]

    for ex in original_model.exchanges:
        if ex.id.startswith("EX_x_") and ex.id not in media:
            ex.bounds = (0, 1000)

    for ex in diel_tomato_model.exchanges:
        if ex.id.startswith("EX_x_") and ex.id.split('_Day')[0].split('_Night')[0] not in media:
            ex.bounds = (0, 1000)

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
