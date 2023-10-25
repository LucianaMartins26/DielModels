import os
import cobra
from tests import TEST_DIR
from cobra.flux_analysis import pfba
import pandas as pd


def validate_ratios(original_model, diel_model):
    original_model.objective = "EX_light"
    original_model.objective_direction = "max"

    original_carboxylation = original_model.reactions.get_by_id("RIBULOSE_BISPHOSPHATE_CARBOXYLASE_RXN_p")
    original_oxygenation = original_model.reactions.get_by_id("RXN_961_c")

    same_flux = original_model.problem.Constraint(
        original_carboxylation.flux_expression * 1 -
        original_oxygenation.flux_expression * 3, lb=0, ub=0)
    original_model.add_cons_vars(same_flux)

    original_solution = pfba(original_model).fluxes

    diel_model.objective = "EX_light_Day"
    diel_model.objective_direction = "max"

    diel_carboxylation_day = diel_model.reactions.get_by_id("RIBULOSE_BISPHOSPHATE_CARBOXYLASE_RXN_p_Day")
    diel_oxygenation_day = diel_model.reactions.get_by_id("RXN_961_c_Day")

    same_flux = diel_model.problem.Constraint(
        diel_carboxylation_day.flux_expression * 1 -
        diel_oxygenation_day.flux_expression * 3, lb=0, ub=0)
    diel_model.add_cons_vars(same_flux)

    diel_carboxylation_night = diel_model.reactions.get_by_id("RIBULOSE_BISPHOSPHATE_CARBOXYLASE_RXN_p_Night")
    diel_oxygenation_night = diel_model.reactions.get_by_id("RXN_961_c_Night")

    same_flux = diel_model.problem.Constraint(
        diel_carboxylation_night.flux_expression * 1 -
        diel_oxygenation_night.flux_expression * 3, lb=0, ub=0)
    diel_model.add_cons_vars(same_flux)

    diel_solution = pfba(diel_model).fluxes

    data = {'Carboxylation/Oxygenation': [original_solution["RIBULOSE_BISPHOSPHATE_CARBOXYLASE_RXN_p_Night"] / original_solution["RXN_961_c"],
                                          diel_solution["RIBULOSE_BISPHOSPHATE_CARBOXYLASE_RXN_p_Day"] / diel_solution["RXN_961_c_Day"],
                                          diel_solution["RIBULOSE_BISPHOSPHATE_CARBOXYLASE_RXN_p_Night"] / diel_solution["RXN_961_c_Night"]]}
    tabel = pd.DataFrame(data)

    tabel.index = ["Populus", "Day Populus", "Night Populus"]

    print(tabel)


if __name__ == '__main__':
    original_model = cobra.io.read_sbml_model(os.path.join(TEST_DIR, 'models', 'Populus_iPop7188.xml'))
    diel_model = cobra.io.read_sbml_model(os.path.join(TEST_DIR, 'models', "diel_populus_model.xml"))

    validate_ratios(original_model, diel_model)
