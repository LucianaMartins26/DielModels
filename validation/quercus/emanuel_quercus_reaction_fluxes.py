import os
import cobra
from tests import TEST_DIR
from cobra.flux_analysis import pfba
import pandas as pd

if __name__ == '__main__':
    emanuel_model = cobra.io.read_sbml_model(os.path.join(TEST_DIR, 'models', 'Emanuel_DielMultiTissueModel.xml'))

    emanuel_model.reactions.get_by_id("EX_Biomass__cyto_Light").bounds = (0.11, 0.11)
    emanuel_model.reactions.EX_C00205__dra_Light.bounds = (-1000, 1000)
    emanuel_model.objective = "EX_C00205__dra_Light"
    emanuel_model.objective_direction = "max"

    diel_multi_carboxylation_day = emanuel_model.reactions.get_by_id("R00024__plst_Leaf_Light")
    diel_multi_oxygenation_day = emanuel_model.reactions.get_by_id("R03140__plst_Leaf_Light")

    same_flux_day = emanuel_model.problem.Constraint(
        diel_multi_carboxylation_day.flux_expression * 1 -
        diel_multi_oxygenation_day.flux_expression * 3, lb=0, ub=0)
    emanuel_model.add_cons_vars(same_flux_day)

    diel_multi_carboxylation_night = emanuel_model.reactions.get_by_id("R00024__plst_Leaf_Dark")
    diel_multi_oxygenation_night = emanuel_model.reactions.get_by_id("R03140__plst_Leaf_Dark")

    same_flux_night = emanuel_model.problem.Constraint(
        diel_multi_carboxylation_night.flux_expression * 1 -
        diel_multi_oxygenation_night.flux_expression * 3, lb=0, ub=0)
    emanuel_model.add_cons_vars(same_flux_night)

    diel_multitissue_solution = pfba(emanuel_model).fluxes

    data = {'RuBisCO + O2': [diel_multitissue_solution["R03140__plst_Leaf_Light"],
                             diel_multitissue_solution["R03140__plst_Leaf_Dark"]],

            'RuBisCO + CO2': [diel_multitissue_solution["R00024__plst_Leaf_Light"],
                              diel_multitissue_solution["R00024__plst_Leaf_Dark"]],

            'Photosystem_I': [diel_multitissue_solution["Photosystem_I__plst_Leaf_Light"],
                              diel_multitissue_solution["Photosystem_I__plst_Leaf_Dark"]],

            'Glicerate-3P to 1,3Bisphosphoglicerate': [diel_multitissue_solution["R01512__plst_Leaf_Light"],
                                                       diel_multitissue_solution["R01512__plst_Leaf_Dark"]],

            '1,3Bisphosphoglicerate to G3P': [diel_multitissue_solution["R01063__plst_Leaf_Light"],
                                              diel_multitissue_solution["R01063__plst_Leaf_Dark"]],

            'G3P to Glycerone-P': [diel_multitissue_solution["R01015__plst_Leaf_Light"],
                                   diel_multitissue_solution["R01015__plst_Leaf_Dark"]],

            'Glycerone-P to Sedoheptulose1,7-bisphosphate': [diel_multitissue_solution["R01829__plst_Leaf_Light"],
                                                             diel_multitissue_solution["R01829__plst_Leaf_Dark"]],

            'Sedoheptulose1,7-bisphosphate to Sedoheptulose7-phosphate': [diel_multitissue_solution[
                                                                              "R01845__plst_Leaf_Light"],
                                                                          diel_multitissue_solution[
                                                                              "R01845__plst_Leaf_Dark"]],

            'Sedoheptulose7-phosphate  to R5P': [diel_multitissue_solution["R01641__plst_Leaf_Light"],
                                                 diel_multitissue_solution["R01641__plst_Leaf_Dark"]],

            'R5P to Ri5P': [diel_multitissue_solution["R01056__plst_Leaf_Light"],
                            diel_multitissue_solution["R01056__plst_Leaf_Dark"]],

            'Ri5P to Ri15P2': [diel_multitissue_solution["R01523__plst_Leaf_Light"],
                               diel_multitissue_solution["R01523__plst_Leaf_Dark"]]
            }

    tabel = pd.DataFrame(data)

    tabel.index = ["Day Emanuel Quercus", "Night Emanuel Quercus"]

    tabel.to_csv('Emanuel_Quercus_Reactions_Fluxes.csv', sep=',')

    print(tabel)
