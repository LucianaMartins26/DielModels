import os
import cobra
from tests import TEST_DIR
from cobra.flux_analysis import pfba
import pandas as pd


def validate_reactions_fluxes(original_model, diel_model, original_multitissue_model, diel_multitissue_model):
    original_model.objective = "EX_C00205__dra"
    original_model.objective_direction = "max"
    original_solution = pfba(original_model).fluxes

    original_multitissue_model.objective = "EX_C00205__dra"
    original_multitissue_model.objective_direction = "max"
    original_multitissue_solution = pfba(original_multitissue_model).fluxes

    diel_model.objective = "EX_C00205__dra_Day"
    diel_model.objective_direction = "max"
    diel_model.reactions.get_by_id("Biomass_Total").bounds = (0,100)
    diel_carboxylation_day = diel_model.reactions.get_by_id("R00024__chlo_Day")
    diel_oxygenation_day = diel_model.reactions.get_by_id("R03140__chlo_Day")

    same_flux = diel_model.problem.Constraint(
        diel_carboxylation_day.flux_expression * 1 -
        diel_oxygenation_day.flux_expression * 3, lb=0, ub=0)
    diel_model.add_cons_vars(same_flux)

    diel_carboxylation_night = diel_model.reactions.get_by_id("R00024__chlo_Night")
    diel_oxygenation_night = diel_model.reactions.get_by_id("R03140__chlo_Night")

    same_flux = diel_model.problem.Constraint(
        diel_carboxylation_night.flux_expression * 1 -
        diel_oxygenation_night.flux_expression * 3, lb=0, ub=0)
    diel_model.add_cons_vars(same_flux)

    diel_solution = pfba(diel_model).fluxes

    diel_multitissue_model.objective = "EX_C00205__dra_Day"
    diel_multitissue_model.objective_direction = "max"
    diel_multitissue_model.reactions.get_by_id("Biomass_Total").bounds = (0, 100)
    diel_multi_carboxylation_day = diel_multitissue_model.reactions.get_by_id("R00024__plst_Leaf_Day")
    diel_multi_oxygenation_day = diel_multitissue_model.reactions.get_by_id("R03140__plst_Leaf_Day")

    same_flux = diel_multitissue_model.problem.Constraint(
        diel_multi_carboxylation_day.flux_expression * 1 -
        diel_multi_oxygenation_day.flux_expression * 3, lb=0, ub=0)
    diel_multitissue_model.add_cons_vars(same_flux)

    diel_multi_carboxylation_night = diel_multitissue_model.reactions.get_by_id("R00024__plst_Leaf_Night")
    diel_multi_oxygenation_night = diel_multitissue_model.reactions.get_by_id("R03140__plst_Leaf_Night")

    same_flux = diel_multitissue_model.problem.Constraint(
        diel_multi_carboxylation_night.flux_expression * 1 -
        diel_multi_oxygenation_night.flux_expression * 3, lb=0, ub=0)
    diel_multitissue_model.add_cons_vars(same_flux)

    diel_multitissue_solution = pfba(diel_multitissue_model).fluxes

    data = {'RuBisCO + O2': [original_solution["R03140__chlo"], original_multitissue_solution["R03140__plst_Leaf"],
                             diel_solution["R03140__chlo_Day"], diel_solution["R03140__chlo_Night"],
                             diel_multitissue_solution["R03140__plst_Leaf_Day"],
                             diel_multitissue_solution["R03140__plst_Leaf_Night"]],

            'RuBisCO + CO2': [original_solution["R00024__chlo"], original_multitissue_solution["R00024__plst_Leaf"],
                              diel_solution["R00024__chlo_Day"], diel_solution["R00024__chlo_Night"],
                              diel_multitissue_solution["R00024__plst_Leaf_Day"],
                              diel_multitissue_solution["R00024__plst_Leaf_Night"]],

            'Photosystem_I': [original_solution["Photosystem_I__chlo"],
                              original_multitissue_solution["Photosystem_I__plst_Leaf"],
                              diel_solution["Photosystem_I__chlo_Day"], diel_solution["Photosystem_I__chlo_Night"],
                              diel_multitissue_solution["Photosystem_I__plst_Leaf_Day"],
                              diel_multitissue_solution["Photosystem_I__plst_Leaf_Night"]],

            'G3P to 1,3Bisphosphoglicerate': [original_solution["R01512__cyto"],
                                              original_multitissue_solution["R01512__plst_Leaf"],
                                              diel_solution["R01512__cyto_Day"], diel_solution["R01512__cyto_Night"],
                                              diel_multitissue_solution["R01512__plst_Leaf_Day"],
                                              diel_multitissue_solution["R01512__plst_Leaf_Night"]],

            '1,3Bisphosphoglicerate to Glyceraldehyde-3P': [original_solution["R01063__chlo"],
                                                            original_multitissue_solution["R01063__plst_Leaf"],
                                                            diel_solution["R01063__chlo_Day"],
                                                            diel_solution["R01063__chlo_Night"],
                                                            diel_multitissue_solution["R01063__plst_Leaf_Day"],
                                                            diel_multitissue_solution["R01063__plst_Leaf_Night"]],

            'Glyceraldehyde-3P to Glycerone-P': [original_solution["R01015__cyto"],
                                                 original_multitissue_solution["R01015__plst_Leaf"],
                                                 diel_solution["R01015__cyto_Day"], diel_solution["R01015__cyto_Night"],
                                                 diel_multitissue_solution["R01015__plst_Leaf_Day"],
                                                 diel_multitissue_solution["R01015__plst_Leaf_Night"]],

            'Glycerone-P to Sedoheptulose1,7-bisphosphate': [original_solution["R01829__cyto"],
                                                             original_multitissue_solution["R01829__plst_Leaf"],
                                                             diel_solution["R01829__cyto_Day"],
                                                             diel_solution["R01829__cyto_Night"],
                                                             diel_multitissue_solution["R01829__plst_Leaf_Day"],
                                                             diel_multitissue_solution["R01829__plst_Leaf_Night"]],

            'Sedoheptulose1,7-bisphosphate to Sedoheptulose7-phosphate': [original_solution["R01845__cyto"],
                                                                          original_multitissue_solution[
                                                                              "R01845__plst_Leaf"],
                                                                          diel_solution["R01845__cyto_Day"],
                                                                          diel_solution["R01845__cyto_Night"],
                                                                          diel_multitissue_solution[
                                                                              "R01845__plst_Leaf_Day"],
                                                                          diel_multitissue_solution[
                                                                              "R01845__plst_Leaf_Night"]],

            'Sedoheptulose7-phosphate  to R5P': [original_solution["R01641__cyto"],
                                                 original_multitissue_solution["R01641__plst_Leaf"],
                                                 diel_solution["R01641__cyto_Day"], diel_solution["R01641__cyto_Night"],
                                                 diel_multitissue_solution["R01641__plst_Leaf_Day"],
                                                 diel_multitissue_solution["R01641__plst_Leaf_Night"]],

            'R5P to Ri5P': [original_solution["R01056__cyto"],
                            original_multitissue_solution["R01056__plst_Leaf"],
                            diel_solution["R01056__cyto_Day"], diel_solution["R01056__cyto_Night"],
                            diel_multitissue_solution["R01056__plst_Leaf_Day"],
                            diel_multitissue_solution["R01056__plst_Leaf_Night"]],

            'Ri5P to Ri15P2': [original_solution["R01523__chlo"],
                               original_multitissue_solution["R01523__plst_Leaf"],
                               diel_solution["R01523__chlo_Day"], diel_solution["R01523__chlo_Night"],
                               diel_multitissue_solution["R01523__plst_Leaf_Day"],
                               diel_multitissue_solution["R01523__plst_Leaf_Night"]]
            }

    tabel = pd.DataFrame(data)

    tabel.index = ["Quercus", "Day Quercus", "Night Quercus", "Quercus Multi Tissue", "Day Multi Quercus",
                   "Night Multi Quercus"]

    tabel.to_csv('Quercus_Reactions_Fluxes.csv', sep=',')

    print(tabel)


if __name__ == '__main__':
    original_model = cobra.io.read_sbml_model(os.path.join(TEST_DIR, 'models', 'QuercusSuberGeneralModel.xml'))
    diel_model = cobra.io.read_sbml_model(os.path.join(TEST_DIR, 'models', "diel_quercus_model.xml"))
    original_multitissue_model = cobra.io.read_sbml_model(
        os.path.join(TEST_DIR, 'models', "MultiTissueQuercusModel.xml"))
    diel_multitissue_model = cobra.io.read_sbml_model(os.path.join(TEST_DIR, 'models', "diel_multi_quercus_model.xml"))

    validate_reactions_fluxes(original_model, diel_model, original_multitissue_model, diel_multitissue_model)
