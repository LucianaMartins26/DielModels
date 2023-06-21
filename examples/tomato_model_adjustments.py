import os
import cobra
from tests import TEST_DIR
import pandas as pd


def tomato_model_adjust(tomato_model):
    ## Reaction bounds setting

    reactions_dict = {}
    for reaction in tomato_model.reactions:
        reactions_dict[reaction.name] = reaction.id

    df = pd.read_excel(os.path.join(TEST_DIR, 'data', 'tpj13075-sup-0013-datafiles3.xlsx'))

    reactions_bounds = []
    for index, row in df.iterrows():
        reaction_name = row['Abbreviation']
        lower_bound = row['Lower bound']
        upper_bound = row['Upper bound']
        reactions_bounds.append((reaction_name, lower_bound, upper_bound))

    for reaction_name, lower_bound, upper_bound in reactions_bounds:
        if reaction_name in reactions_dict:
            reaction_id = reactions_dict[reaction_name]
            reaction = tomato_model.reactions.get_by_id(reaction_id)
            reaction.upper_bound = upper_bound
            reaction.lower_bound = lower_bound
        else:
            print(f"Not possible to find: {reaction_name}")

    ## Create biomass metabolite and it's exchange reaction

    biomass_metabolite = cobra.Metabolite(
        "x_biomass",
        formula=None,
        name="biomass",
        compartment="DefaultCompartment",
    )

    biomass_metabolite_rxn = cobra.Reaction("EX_x_biomass")
    biomass_metabolite_rxn.name = "Biomass exchange reaction"
    biomass_metabolite_rxn.bounds = (0, 1000000)

    biomass_metabolite_rxn.add_metabolites({
        biomass_metabolite: -1})

    tomato_model.add_reactions([biomass_metabolite_rxn])

    tomato_model.add_metabolites(biomass_metabolite)

    ## Create biomass reaction

    bm_met_df = pd.read_excel(os.path.join(TEST_DIR, 'data', 'Biomass_Reactions.xlsx'))
    coef_dict = dict(zip(bm_met_df["Component"], bm_met_df["Coefficient"]))

    biomass_rxn = cobra.Reaction("biomass_reaction")

    for met, coef in coef_dict.items():
        biomass_rxn.add_metabolites({tomato_model.metabolites.get_by_id(met): -float(coef)})

    biomass_rxn.add_metabolites({biomass_metabolite: 1})
    tomato_model.add_reactions([biomass_rxn])

    ## Define objective function

    tomato_model.objective = tomato_model.reactions.get_by_id("EX_x_Photon")

    cobra.io.write_sbml_model(tomato_model, os.path.join(TEST_DIR, 'data', 'functional_tomato_model.xml'))


if __name__ == '__main__':
    tomato_model_path = os.path.join(TEST_DIR, 'data', 'tpj13075-sup-0011-DataFileS1.xml')
    tomato_model = cobra.io.read_sbml_model(tomato_model_path)
    tomato_model_adjust(tomato_model)
