import os
import cobra
from tests import TEST_DIR
from cobra.flux_analysis import pfba
import pandas as pd


def validate_ratios(original_model, diel_model):
    original_model.objective = "EX11"
    original_model.objective_direction = "max"

    original_carboxylation = original_model.reactions.get_by_id("R00024_p")
    original_oxygenation = original_model.reactions.get_by_id("R03140_p")

    same_flux = original_model.problem.Constraint(
        original_carboxylation.flux_expression * 1 -
        original_oxygenation.flux_expression * 3, lb=0, ub=0)
    original_model.add_cons_vars(same_flux)

    original_solution = pfba(original_model).fluxes

    diel_model.objective = "EX11_Day"
    diel_model.objective_direction = "max"

    diel_carboxylation_day = diel_model.reactions.get_by_id("R00024_p_Day")
    diel_oxygenation_day = diel_model.reactions.get_by_id("R03140_p_Day")

    same_flux = diel_model.problem.Constraint(
        diel_carboxylation_day.flux_expression * 1 -
        diel_oxygenation_day.flux_expression * 3, lb=0, ub=0)
    diel_model.add_cons_vars(same_flux)

    diel_carboxylation_night = diel_model.reactions.get_by_id("R00024_p_Night")
    diel_oxygenation_night = diel_model.reactions.get_by_id("R03140_p_Night")

    same_flux = diel_model.problem.Constraint(
        diel_carboxylation_night.flux_expression * 1 -
        diel_oxygenation_night.flux_expression * 3, lb=0, ub=0)
    diel_model.add_cons_vars(same_flux)

    diel_solution = pfba(diel_model).fluxes

    data = {'Carboxylation/Oxygenation': [original_solution["R00024_p"] / original_solution["R03140_p"],
                                          diel_solution["R00024_p_Day"] / diel_solution["R03140_p_Day"],
                                          diel_solution["R00024_p_Night"] / diel_solution["R03140_p_Night"]]}
    tabel = pd.DataFrame(data)

    tabel.index = ["C4GEM", "Day C4GEM", "Night C4GEM"]

    print(tabel)


if __name__ == '__main__':
    original_maize_C4GEM_model = cobra.io.read_sbml_model(os.path.join(TEST_DIR, 'models', 'Maize_C4GEM_vs1.0.xml'))
    diel_maize_C4GEM_model = cobra.io.read_sbml_model(os.path.join(TEST_DIR, 'models', "diel_maizeC4GEM_model.xml"))

    original_sorghum_C4GEM_model = cobra.io.read_sbml_model(os.path.join(TEST_DIR, 'models', 'Sorghum_C4GEM_vs1.0.xml'))
    diel_sorghum_C4GEM_model = cobra.io.read_sbml_model(os.path.join(TEST_DIR, 'models', 'diel_sorghum_model.xml'))

    original_sugarcane_C4GEM_model = cobra.io.read_sbml_model(os.path.join(TEST_DIR, 'models', 'SugarCane_C4GEM_vs1.0.xml'))
    diel_sugarcane_C4GEM_model = cobra.io.read_sbml_model(os.path.join(TEST_DIR, 'models', 'diel_sugarcane_model.xml'))

    print(f"Maize: {validate_ratios(original_maize_C4GEM_model, diel_maize_C4GEM_model)}")
    print(f"Sorghum: {validate_ratios(original_sorghum_C4GEM_model, diel_sorghum_C4GEM_model)}")
    print(f"SugarCane: {validate_ratios(original_sugarcane_C4GEM_model, diel_sugarcane_C4GEM_model)}")

