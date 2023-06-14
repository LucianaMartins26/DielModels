import os
import cobra
from tests import TEST_DIR
from cobra.flux_analysis import pfba


def validate_reactions_fluxes(original_model, diel_model):
    original_model.objective = "biomass_reaction"
    original_model.reactions.get_by_id("biomass_reaction").bounds = (0.11, 0.11)
    original_model.reactions.get_by_id("ATPase_Cyto").bounds = (7.1, 7.1)
    original_model.objective_direction = "min"
    original_solution = pfba(original_model).fluxes

    diel_model.objective = "Biomass_Total"
    diel_model.reactions.get_by_id("Biomass_Total").bounds = (0.11, 0.11)
    diel_model.reactions.get_by_id("ATPase_Cyto_Day").bounds = (7.1, 7.1)
    diel_model.objective_direction = "min"
    diel_solution = pfba(diel_model).fluxes

    print(f'Photon Drain: {original_solution["EX_x_Photon"]}, {diel_solution["EX_x_Photon_Day"]}, '
          f'{diel_solution["EX_x_Photon_Night"]}')

    print(f'Photon reaction 1: {original_solution["reac_1017"]}, {diel_solution["reac_1017_Day"]}, '
          f'{diel_solution["reac_1017_Night"]}')

    print(f'Photon reaction 2: {original_solution["reac_1883"]}, {diel_solution["reac_1883_Day"]}, '
          f'{diel_solution["reac_1883_Night"]}')

    print(f'Photon reaction 3: {original_solution["Photon_tx"]}, {diel_solution["Photon_tx_Day"]}, '
          f'{diel_solution["Photon_tx_Night"]}')

    print(f'RuBisCO + CO2: {original_solution["reac_1070"]}, {diel_solution["reac_1070_Day"]}, '
          f'{diel_solution["reac_1070_Night"]}')

    print(f'RuBisCO + O2: {original_solution["reac_1742"]}, {diel_solution["reac_1742_Day"]}, '
          f'{diel_solution["reac_1742_Night"]}')

    print(f'G3P to 1,3BPG: {original_solution["reac_972"]}, {diel_solution["reac_972_Day"]}, '
          f'{diel_solution["reac_972_Night"]}')

    print(f'1,3BPG to GAP: {original_solution["reac_30"]}, {diel_solution["reac_30_Day"]}, '
          f'{diel_solution["reac_30_Night"]}')

    print(f'GAP to Ribulose-5P: {original_solution["reac_60"]}, {diel_solution["reac_60_Day"]}, '
          f'{diel_solution["reac_60_Night"]}')

    print(f'Ribose-5P to Ribulose-5P: {original_solution["reac_1063"]}, {diel_solution["reac_1063_Day"]}, '
          f'{diel_solution["reac_1063_Night"]}')

    print(f'Ribulose-5P to Ribulose-1,5P: {original_solution["reac_977"]}, {diel_solution["reac_977_Day"]}, '
          f'{diel_solution["reac_977_Night"]}')


if __name__ == '__main__':
    tomato_diel_model_path = os.path.join(TEST_DIR, 'data', 'diel_tomato_model.xml')
    tomato_diel_model = cobra.io.read_sbml_model(tomato_diel_model_path)

    tomato_original_model_path = os.path.join(TEST_DIR, 'data', 'functional_tomato_model.xml')
    tomato_original_model = cobra.io.read_sbml_model(tomato_original_model_path)

    validate_reactions_fluxes(tomato_original_model, tomato_diel_model)
