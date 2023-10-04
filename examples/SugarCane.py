import cobra
import os
from tests import TEST_DIR
from diel_models.diel_models_creator import diel_models_creator
import pandas as pd


def diel_sugarcane(model):
    biomass_metabolite = cobra.Metabolite(
        "x_biomass",
        formula=None,
        name="biomass",
        compartment="C_biomass",
    )

    biomass_metabolite_rxn = cobra.Reaction("EX_x_biomass")
    biomass_metabolite_rxn.name = "Biomass exchange reaction"
    biomass_metabolite_rxn.bounds = (0, 1000000)

    biomass_metabolite_rxn.add_metabolites({biomass_metabolite: -1})

    model.add_reactions([biomass_metabolite_rxn])

    model.add_metabolites(biomass_metabolite)

    bm_met_df = pd.read_excel(os.path.join(TEST_DIR, 'models', 'C4GEM_Biomass_Reactions.xlsx'))
    coef_dict = dict(zip(bm_met_df["Component"], bm_met_df["Coefficient"]))

    biomass_rxn = cobra.Reaction("Biomass_rxn")
    biomass_rxn.name = "Biomass Reaction"

    for met, coef in coef_dict.items():
        biomass_rxn.add_metabolites({model.metabolites.get_by_id(met): -float(coef)})

    biomass_rxn.add_metabolites({biomass_metabolite: 1, model.metabolites.get_by_id("S_ADP_c"): 30,
                                 model.metabolites.get_by_id("S_Orthophosphate_c"): 30})

    model.add_reactions([biomass_rxn])

    diel_models_creator(model,
                        ["S_Sucrose_c", "S_Sulfate_c", "S_Nitrate_c", "S_L_45_Histidine_c", "S_L_45_Isoleucine_c",
                         "S_L_45_Leucine_c", "S_L_45_Lysine_c", "S_L_45_Methionine_c", "S_L_45_Phenylalanine_c",
                         "S_L_45_Tryptophan_c", "S_L_45_Threonine_c", "S_L_45_Valine_c", "S_L_45_Asparagine_c",
                         "S_L_45_Cystine_c", "S_L_45_Glutamine_c", "S_Glycine_c", "S_L_45_Proline_c",
                         "S_L_45_Tyrosine_c", "S_Glutamate_c", "S_L_45_Alanine_c", "S_L_45_Aspartate_c",
                         "S_L_45_Serine_c", "S_Starch_p", "S_beta_45_D_45_Fructose_c", "S__40_S_41__45_Malate_c",
                         "S_Fumarate_c", "S_Citrate_c"], ["EX11"], "Biomass_rxn", ["EX_S_Nitrate_ext"])

    cobra.io.write_sbml_model(model, os.path.join(TEST_DIR, 'models', 'diel_sugarcane_model.xml'))


if __name__ == '__main__':
    sugarcane_model_path = os.path.join(TEST_DIR, 'models', 'SugarCane_C4GEM_vs1.0.xml')
    sugarcane_model = cobra.io.read_sbml_model(sugarcane_model_path)
    diel_sugarcane(sugarcane_model)
