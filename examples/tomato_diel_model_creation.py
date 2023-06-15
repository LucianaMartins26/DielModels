import os
import cobra
from tests import TEST_DIR
import pandas as pd
from diel_models.diel_models_creator import diel_models_creator


def diel_model(model):

    diel_models_creator(model, ["x_Starch"], 'EX_x_Photon', 'biomass_reaction', 'EX_x_NO3')

    model.reactions.get_by_id("EX_x_CO2_Day").bounds = (-1000000, 0)
    model.reactions.get_by_id("EX_x_CO2_Night").bounds = (0, 1000000)

    model.reactions.get_by_id("EX_x_O2_Day").bounds = (0, 1000000)
    model.reactions.get_by_id("EX_x_O2_Night").bounds = (-1000000, 0)

    model.reactions.get_by_id("EX_x_SUCROSE_Day").bounds = (0, 1000000)
    model.reactions.get_by_id("EX_x_SUCROSE_Night").bounds = (0, 1000000)

    model.reactions.get_by_id("EX_x_Cellulose_Day").bounds = (0, 1000000)
    model.reactions.get_by_id("EX_x_Cellulose_Night").bounds = (0, 1000000)

    model.reactions.get_by_id("Starch_bm_tx_Day").bounds = (-1000000, 0)
    model.reactions.get_by_id("Starch_bm_tx_Night").bounds = (0, 1000000)

    model.reactions.get_by_id("EX_x_UMP_Day").bounds = (0, 1000000)
    model.reactions.get_by_id("EX_x_UMP_Night").bounds = (0, 0)

    model.reactions.get_by_id("EX_x_Starch_Day").bounds = (-1000000, 0)
    model.reactions.get_by_id("EX_x_Starch_Night").bounds = (0, 1000000)

    df = pd.read_excel(os.path.join(TEST_DIR, 'data', 'Photoautotrophic conditions.xlsx'))

    for reaction in df.iterrows():
        model.reactions.get_by_id(reaction[1]['Reaction']).bounds = (reaction[1]['lb'], reaction[1]['ub'])

    cobra.io.write_sbml_model(model, os.path.join(TEST_DIR, 'data', 'diel_tomato_model.xml'))


if __name__ == '__main__':
    tomato_model_path = os.path.join(TEST_DIR, 'data', 'functional_tomato_model.xml')
    tomato_model = cobra.io.read_sbml_model(tomato_model_path)
    diel_model(tomato_model)
