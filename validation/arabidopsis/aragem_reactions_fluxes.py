import os
import cobra
from tests import TEST_DIR
from cobra.flux_analysis import pfba


def validate_reactions_fluxes(original_model, diel_model):
    original_model.objective = "Ex16"
    original_model.objective_direction = "max"

    original_model_carboxylation = original_model.reactions.get_by_id("R00024_p")
    original_model_oxygenation = original_model.reactions.get_by_id("R03140_p")

    same_flux = original_model.problem.Constraint(
        original_model_carboxylation.flux_expression * 1 -
        original_model_oxygenation.flux_expression * 3, lb=0, ub=0)
    original_model.add_cons_vars(same_flux)

    original_solution = pfba(original_model).fluxes

    diel_model.objective = "Ex16_Day"
    diel_model.objective_direction = "max"
    diel_model.reactions.get_by_id("Biomass_Total").lower_bound = 0.11
    diel_model.reactions.get_by_id("Biomass_Total").upper_bound = 0.11

    diel_model_carboxylation = diel_model.reactions.get_by_id("R00024_p_Day")
    diel_model_oxygenation = diel_model.reactions.get_by_id("R03140_p_Day")

    same_flux = diel_model.problem.Constraint(
        diel_model_carboxylation.flux_expression * 1 -
        diel_model_oxygenation.flux_expression * 3, lb=0, ub=0)
    diel_model.add_cons_vars(same_flux)

    diel_solution = pfba(diel_model).fluxes

    print(f'Photosynthesis: {original_solution["REner01_p"]}, {diel_solution["REner01_p_Day"]}, '
          f'{diel_solution["REner01_p_Night"]}')

    print(f'RuBisCO + CO2: {original_solution["R00024_p"]}, {diel_solution["R00024_p_Day"]}, '
          f'{diel_solution["R00024_p_Night"]}')

    print(f'RuBisCO + O2: {original_solution["R03140_p"]}, {diel_solution["R03140_p_Day"]}, '
          f'{diel_solution["R03140_p_Night"]}')

    print(f'G3P to 1,3BPG: {original_solution["R01512_p"]}, {diel_solution["R01512_p_Day"]}, '
          f'{diel_solution["R01512_p_Night"]}')

    print(f'1,3BPG to GAP: {original_solution["R01063_p"]}, {diel_solution["R01063_p_Day"]}, '
          f'{diel_solution["R01063_p_Night"]}')

    print(f'GAP to Ribulose-5P: {original_solution["R01641_p"]}, {diel_solution["R01641_p_Day"]}, '
          f'{diel_solution["R01641_p_Night"]}')

    print(f'Ribose-5P to Ribulose-5P: {original_solution["R01056_p"]}, {diel_solution["R01056_p_Day"]}, '
          f'{diel_solution["R01056_p_Night"]}')

    print(f'Ribulose-5P to Ribulose-1,5P: {original_solution["R01523_p"]}, {diel_solution["R01523_p_Day"]}, '
          f'{diel_solution["R01523_p_Night"]}')


if __name__ == '__main__':
    diel_model_path = os.path.join(TEST_DIR, 'reconstruction_results', 'MODEL1507180028', 'results_troppo', 'DielModel',
                              'reconstructed_models', 'Diel_Model.xml')

    diel_model = cobra.io.read_sbml_model(diel_model_path)

    original_model = cobra.io.read_sbml_model(os.path.join(TEST_DIR, 'data', 'aragem_photo.xml'))

    validate_reactions_fluxes(original_model, diel_model)
