import os
import cobra
from tests import TEST_DIR
from cobra.flux_analysis import pfba
import pandas as pd


def validate_ratios(original_model, diel_model, original_multitissue_model, diel_multitissue_model):
    original_model.objective = "EX_C00205__dra"
    original_model.objective_direction = "max"
    original_solution = pfba(original_model).fluxes

    original_multitissue_model.objective = "EX_C00205__dra"
    original_multitissue_model.objective_direction = "max"
    original_multitissue_solution = pfba(original_multitissue_model).fluxes

    diel_model.objective = "EX_C00205__dra_Day"
    diel_model.objective_direction = "max"
    diel_model.reactions.get_by_id("Biomass_Total").lower_bound = 0.20
    diel_model.reactions.get_by_id("Biomass_Total").upper_bound = 0.20
    diel_solution = pfba(diel_model).fluxes

    diel_multitissue_model.objective = "EX_C00205__dra_Day"
    diel_multitissue_model.objective_direction = "max"
    diel_multitissue_solution = pfba(diel_multitissue_model).fluxes

    original_carboxylation = original_model.reactions.get_by_id("R00024__chlo")
    original_oxygenation = original_model.reactions.get_by_id("R03140__chlo")

    same_flux = original_model.problem.Constraint(
        original_carboxylation.flux_expression * 1 -
        original_oxygenation.flux_expression * 3, lb=0, ub=0)
    original_model.add_cons_vars(same_flux)

    diel_carboxylation = diel_model.reactions.get_by_id("R00024__chlo_Day")
    diel_oxygenation = diel_model.reactions.get_by_id("R03140__chlo_Day")

    same_flux = diel_model.problem.Constraint(
        diel_carboxylation.flux_expression * 1 -
        diel_oxygenation.flux_expression * 3, lb=0, ub=0)
    diel_model.add_cons_vars(same_flux)

    multi_carboxylation = original_multitissue_model.reactions.get_by_id("R00024__plst_Leaf")
    multi_oxygenation = original_multitissue_model.reactions.get_by_id("R03140__plst_Leaf")

    same_flux = original_multitissue_model.problem.Constraint(
        multi_carboxylation.flux_expression * 1 -
        multi_oxygenation.flux_expression * 3, lb=0, ub=0)
    original_multitissue_model.add_cons_vars(same_flux)

    diel_multi_carboxylation = diel_multitissue_model.reactions.get_by_id("R00024__plst_Leaf_Day")
    diel_multi_oxygenation = diel_multitissue_model.reactions.get_by_id("R03140__plst_Leaf_Day")

    same_flux = diel_multitissue_model.problem.Constraint(
        diel_multi_carboxylation.flux_expression * 1 -
        diel_multi_oxygenation.flux_expression * 3, lb=0, ub=0)
    diel_multitissue_model.add_cons_vars(same_flux)

    data = {'Carboxylation/Oxygenation': [original_solution["R00024__chlo"] / original_solution["R03140__chlo"],
                                          original_multitissue_solution["R00024__plst_Leaf"] /
                                          original_multitissue_solution["R03140__plst_Leaf"],
                                          diel_solution["R00024__chlo_Day"] / diel_solution["R03140__chlo_Day"],
                                          diel_solution["R00024__chlo_Night"] / diel_solution["R03140__chlo_Night"],
                                          diel_multitissue_solution["R00024__plst_Leaf_Day"] /
                                          diel_multitissue_solution["R03140__plst_Leaf_Day"],
                                          diel_multitissue_solution["R00024__plst_Leaf_Night"] /
                                          diel_multitissue_solution["R03140__plst_Leaf_Night"]]}

    tabel = pd.DataFrame(data)

    tabel.index = ["Quercus", "Quercus Multi Tissue", "Day Quercus", "Night Quercus", "Day Multi Quercus",
                   "Night Multi Quercus"]

    print(tabel)


if __name__ == '__main__':
    original_model = cobra.io.read_sbml_model(os.path.join(TEST_DIR, 'models', 'QuercusSuberGeneralModel.xml'))
    diel_model = cobra.io.read_sbml_model(os.path.join(TEST_DIR, 'models', "diel_quercus_model.xml"))
    original_multitissue_model = cobra.io.read_sbml_model(
        os.path.join(TEST_DIR, 'models', "MultiTissueQuercusModel.xml"))
    diel_multitissue_model = cobra.io.read_sbml_model(os.path.join(TEST_DIR, 'models', "diel_multi_quercus_model.xml"))

    validate_ratios(original_model, diel_model, original_multitissue_model, diel_multitissue_model)
