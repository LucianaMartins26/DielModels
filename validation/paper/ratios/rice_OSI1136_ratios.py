import os
import cobra
from tests import TEST_DIR
from cobra.flux_analysis import pfba
import pandas as pd


def validate_ratios(original_model, diel_model):
    original_model.objective = "chl_Photon_tx"
    original_model.objective_direction = "max"

    original_carboxylation = original_model.reactions.get_by_id("chl_Rubisco")
    original_oxygenation = original_model.reactions.get_by_id("chl_RuBPOxid")

    same_flux = original_model.problem.Constraint(
        original_carboxylation.flux_expression * 1 -
        original_oxygenation.flux_expression * 3, lb=0, ub=0)
    original_model.add_cons_vars(same_flux)

    original_solution = pfba(original_model).fluxes

    diel_model.objective = "chl_Photon_tx_Day"
    diel_model.objective_direction = "max"

    diel_carboxylation_day = diel_model.reactions.get_by_id("chl_Rubisco_Day")
    diel_oxygenation_day = diel_model.reactions.get_by_id("chl_RuBPOxid_Day")

    same_flux = diel_model.problem.Constraint(
        diel_carboxylation_day.flux_expression * 1 -
        diel_oxygenation_day.flux_expression * 3, lb=0, ub=0)
    diel_model.add_cons_vars(same_flux)

    diel_carboxylation_night = diel_model.reactions.get_by_id("chl_Rubisco_Night")
    diel_oxygenation_night = diel_model.reactions.get_by_id("chl_RuBPOxid_Night")

    same_flux = diel_model.problem.Constraint(
        diel_carboxylation_night.flux_expression * 1 -
        diel_oxygenation_night.flux_expression * 3, lb=0, ub=0)
    diel_model.add_cons_vars(same_flux)

    diel_solution = pfba(diel_model).fluxes

    data = {'Carboxylation/Oxygenation': [original_solution["chl_Rubisco"] / original_solution["chl_RuBPOxid"],
                                          diel_solution["chl_Rubisco_Day"] / diel_solution["chl_RuBPOxid_Day"],
                                          diel_solution["chl_Rubisco_Night"] / diel_solution["chl_RuBPOxid_Night"]]}
    tabel = pd.DataFrame(data)

    tabel.index = ["Rice OSI1136", "Day Rice OSI1136", "Night Rice OSI1136"]

    print(tabel)


if __name__ == '__main__':
    original_model = cobra.io.read_sbml_model(os.path.join(TEST_DIR, 'models', 'Rice_OSI1136.sbml'))
    diel_model = cobra.io.read_sbml_model(os.path.join(TEST_DIR, 'models', "diel_rice_OSI1136_model.xml"))

    validate_ratios(original_model, diel_model)
