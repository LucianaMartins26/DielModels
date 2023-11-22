import os
import cobra
from tests import TEST_DIR
from cobra.flux_analysis import pfba
import pandas as pd


def validate_ratios(original_model, diel_model):
    original_model.objective = "RB002"
    original_model.objective_direction = "max"

    original_carboxylation = original_model.reactions.get_by_id("R00024")
    original_oxygenation = original_model.reactions.get_by_id("R03140")

    same_flux = original_model.problem.Constraint(
        original_carboxylation.flux_expression * 1 -
        original_oxygenation.flux_expression * 3, lb=0, ub=0)
    original_model.add_cons_vars(same_flux)

    original_solution = pfba(original_model).fluxes

    diel_model.objective = "RB002_Day"
    diel_model.objective_direction = "max"
    diel_model.reactions.get_by_id("Biomass_Total").lower_bound = 20
    diel_model.reactions.get_by_id("Biomass_Total").upper_bound = 20

    diel_carboxylation_day = diel_model.reactions.get_by_id("R00024_Day")
    diel_oxygenation_day = diel_model.reactions.get_by_id("R03140_Day")

    same_flux = diel_model.problem.Constraint(
        diel_carboxylation_day.flux_expression * 1 -
        diel_oxygenation_day.flux_expression * 3, lb=0, ub=0)
    diel_model.add_cons_vars(same_flux)

    diel_carboxylation_night = diel_model.reactions.get_by_id("R00024_Night")
    diel_oxygenation_night = diel_model.reactions.get_by_id("R03140_Night")

    same_flux = diel_model.problem.Constraint(
        diel_carboxylation_night.flux_expression * 1 -
        diel_oxygenation_night.flux_expression * 3, lb=0, ub=0)
    diel_model.add_cons_vars(same_flux)

    diel_solution = pfba(diel_model).fluxes

    data = {'Carboxylation/Oxygenation': [original_solution["R00024"] / original_solution["R03140"],
                                          diel_solution["R00024_Day"] / diel_solution["R03140_Day"],
                                          diel_solution["R00024_Night"] / diel_solution["R03140_Night"]]}
    tabel = pd.DataFrame(data)

    tabel.index = ["Potato", "Day Potato", "Night Potato"]

    print(tabel)


if __name__ == '__main__':
    original_model = cobra.io.read_sbml_model(os.path.join(TEST_DIR, 'models', 'potato_mat.xml'))
    diel_model = cobra.io.read_sbml_model(os.path.join(TEST_DIR, 'models', "diel_potato_model.xml"))

    validate_ratios(original_model, diel_model)
