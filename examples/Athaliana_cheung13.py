import cobra
import os

import pandas as pd

from tests import TEST_DIR
from diel_models.diel_models_creator import diel_models_creator


def diel_thaliana2013(model):

    biomass_reactions = []
    for reaction in model.reactions:
        if "biomass" in reaction.name:
            biomass_reactions.append(reaction.id)

    biomass_rxn = cobra.Reaction("Biomass_rxn")
    biomass_rxn.name = "Biomass reaction"

    for reacao_id in biomass_reactions:
        reacao_individual = model.reactions.get_by_id(reacao_id)
        biomass_rxn.add_metabolites(
            {metabolito: -coeficiente for metabolito, coeficiente in reacao_individual.metabolites.items()})
        reacao_individual.knock_out()

    model.add_reactions([biomass_rxn])

    constraints_for_simulations_1 = pd.read_excel(os.path.join(TEST_DIR, 'models', 'constraints_for_simulations_1.xlsx'))

    bounds_dict = dict(zip(constraints_for_simulations_1["Reaction"], constraints_for_simulations_1["Control"]))

    for reaction, bound in bounds_dict.items():
        model.reactions.get_by_id(reaction).bounds = (bound, 1000)

    for reaction in biomass_reactions:
        if reaction not in bounds_dict.keys():
            model.reactions.get_by_id(reaction).bounds = (0, 0)

    constraints_for_simulations_2 = pd.read_excel(os.path.join(TEST_DIR, 'models', 'constraints_for_simulations_2.xlsx'))

    for reaction, lower_bound, upper_bound in zip(constraints_for_simulations_2["Reaction"].tolist(),
                                                  constraints_for_simulations_2["Minimum"].tolist(),
                                                  constraints_for_simulations_2["Maximum"].tolist()):
        model.reactions.get_by_id(reaction).bounds = (lower_bound, upper_bound)

    flux_1 = model.problem.Constraint(
        model.reactions.get_by_id("NO3_tx").flux_expression * 1 -
        model.reactions.get_by_id("NH4_tx").flux_expression * 1, lb=0, ub=0)
    model.add_cons_vars(flux_1)

    flux_2 = model.problem.Constraint(
        model.reactions.get_by_id("NADPHoxc_tx").flux_expression * 1 -
        model.reactions.get_by_id("NADPHoxp_tx").flux_expression * 1 -
        model.reactions.get_by_id("NADPHoxm_tx").flux_expression * 1, lb=0, ub=0)
    model.add_cons_vars(flux_2)

    model.objective = model.reactions.get_by_id("EX_x_Photon")

    for compartment_id in model.compartments:
        model._compartments[compartment_id] = compartment_id

    diel_models_creator(model,
                        ["SUCROSE_c", "SULFATE_c", "NITRATE_c", "HIS_c", "ILE_c",
                         "LEU_c", "LYS_c", "MET_c", "PHE_c", "THR_c", "TRP_c", "VAL_c",
                         "ARG_c", "CYS_c", "GLN_c", "GLY_c", "PRO_c", "TYR_c", "met_2041",
                         "met_2074", "ASN_c", "SER_c", "STARCH_p", "FRU_c", "MAL_c",
                         "FUM_c", "CIT_c"], ["EX_x_Photon"], "Biomass_rxn",
                        ["EX_x_NO3"])

    cobra.io.write_sbml_model(model, os.path.join(TEST_DIR, 'models', 'diel_thaliana2013_model.xml'))


if __name__ == '__main__':
    thaliana2013_model_path = os.path.join(TEST_DIR, 'models', 'Athaliana_cheung13.xml')
    thaliana2013_model = cobra.io.read_sbml_model(thaliana2013_model_path)
    diel_thaliana2013(thaliana2013_model)