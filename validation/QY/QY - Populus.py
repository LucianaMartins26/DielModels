import os

import cobra
import pandas as pd

from cobra.flux_analysis import pfba
from tests import TEST_DIR


def QY(non_diel_model, diel_model):
    fba_sol_non_diel = pfba(non_diel_model).fluxes
    fba_sol_diel_model = pfba(diel_model).fluxes

    return fba_sol_non_diel, fba_sol_diel_model


def remove_metabolite(model, biomass_reaction, metabolites_list):
    for metabolite in metabolites_list:
        stoichiometry = model.reactions.get_by_id(biomass_reaction).metabolites[model.metabolites.get_by_id(metabolite)]
        model.reactions.get_by_id(biomass_reaction).add_metabolites(
            {model.metabolites.get_by_id(metabolite): -stoichiometry})
    return model


if __name__ == '__main__':
    original_model = cobra.io.read_sbml_model(os.path.join(TEST_DIR, 'models', 'Populus_iPop7188_fixed.xml'))
    diel_populus_model = cobra.io.read_sbml_model(os.path.join(TEST_DIR, 'models', "diel_populus_model_fixed.xml"))

    diel_populus_model = remove_metabolite(diel_populus_model, "Biomass_Total",
                                           ["cpd1f_118_p_Night", "cpd1f_126_p_Night", "cpd_693_p_Night"])

    original_model.objective = "EX_light"
    original_model.objective_direction = "max"
    original_model.reactions.BiomassRxn.bounds = (0.11, 0.11)
    diel_populus_model.reactions.Biomass_Total.bounds = (0.11, 0.11)
    diel_populus_model.objective = "EX_light_Day"
    diel_populus_model.objective_direction = "max"

    fba_sol_non_diel, fba_sol_diel_model = QY(original_model, diel_populus_model)

    data_quantum_assimilation = {
        'Quantum Yield': [fba_sol_non_diel["RIBULOSE_BISPHOSPHATE_CARBOXYLASE_RXN_p"] / - fba_sol_non_diel["EX_light"],
                          fba_sol_diel_model["RIBULOSE_BISPHOSPHATE_CARBOXYLASE_RXN_p_Day"] / - fba_sol_diel_model[
                              "EX_light_Day"]]}

    tabel = pd.DataFrame(data_quantum_assimilation)

    tabel.index = ["Original Model", "Created Diel Model"]

    tabel.to_csv('QY_Populus.csv', sep=',')

    print(tabel)
