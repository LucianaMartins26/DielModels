import cobra
import os

from tests import TEST_DIR

if __name__ == '__main__':
    luciana_diel_model = cobra.io.read_sbml_model(os.path.join(TEST_DIR, 'models', "diel_multi_quercus_model.xml"))

    Biomass_Total = luciana_diel_model.reactions.get_by_id('Biomass_Total')
    Total_biomass_Day = luciana_diel_model.reactions.get_by_id('Total_biomass_Day')
    Total_biomass_Night = luciana_diel_model.reactions.get_by_id('Total_biomass_Night')
    EX_Total_biomass_Day = luciana_diel_model.reactions.get_by_id('EX_Total_biomass_Day')
    EX_Total_biomass_Night = luciana_diel_model.reactions.get_by_id('EX_Total_biomass_Night')
    EX_Leaf_Day = luciana_diel_model.reactions.get_by_id('EX_Leaf_Day')
    EX_Leaf_Night = luciana_diel_model.reactions.get_by_id('EX_Leaf_Night')
    EX_Phellogen_Day = luciana_diel_model.reactions.get_by_id('EX_Phellogen_Day')
    EX_Phellogen_Night = luciana_diel_model.reactions.get_by_id('EX_Phellogen_Night')
    EX_Ibark_Day = luciana_diel_model.reactions.get_by_id('EX_Ibark_Day')
    EX_Ibark_Night = luciana_diel_model.reactions.get_by_id('EX_Ibark_Night')

    luciana_diel_model.remove_reactions([Biomass_Total, Total_biomass_Day,
                                         Total_biomass_Night, EX_Total_biomass_Day,
                                         EX_Total_biomass_Night, EX_Leaf_Day, EX_Leaf_Night,
                                         EX_Phellogen_Day, EX_Phellogen_Night, EX_Ibark_Day,
                                         EX_Ibark_Night])

    Leaf_biomass_met = cobra.Metabolite(
        "Leaf_biomass",
        name="Leaf Biomass",
        compartment="C_00011"
    )

    Phellogen_biomass_met = cobra.Metabolite(
        "Phellogen_biomass",
        name="Phellogen Biomass",
        compartment="C_00011"
    )

    Ibark_biomass_met = cobra.Metabolite(
        "Ibark_biomass",
        name="Ibark Biomass",
        compartment="C_00011"
    )

    Total_biomass_met = cobra.Metabolite(
        "Total_biomass",
        name="Total Biomass",
        compartment="C_00011"
    )

    luciana_diel_model.add_metabolites([Leaf_biomass_met, Phellogen_biomass_met, Ibark_biomass_met, Total_biomass_met])

    leaf_biomass_reaction = cobra.Reaction("Leaf_biomass")

    leaf_biomass_reaction.add_metabolites({
        luciana_diel_model.metabolites.get_by_id('M8410__cyto_Leaf_Day'): -1.0,
        luciana_diel_model.metabolites.get_by_id('M8410__cyto_Leaf_Night'): -1.0,
        luciana_diel_model.metabolites.get_by_id('Leaf_biomass'): 1.0,
    })

    phellogen_biomass_reaction = cobra.Reaction("Phellogen_biomass")

    phellogen_biomass_reaction.add_metabolites({
        luciana_diel_model.metabolites.get_by_id('M8410__cyto_Phellogen_Day'): -1.0,
        luciana_diel_model.metabolites.get_by_id('M8410__cyto_Phellogen_Night'): -1.0,
        luciana_diel_model.metabolites.get_by_id('Phellogen_biomass'): 1.0,
    })

    ibark_biomass_reaction = cobra.Reaction("Ibark_biomass")

    ibark_biomass_reaction.add_metabolites({
        luciana_diel_model.metabolites.get_by_id('M8410__cyto_Ibark_Day'): -1.0,
        luciana_diel_model.metabolites.get_by_id('M8410__cyto_Ibark_Night'): -1.0,
        luciana_diel_model.metabolites.get_by_id('Ibark_biomass'): 1.0,
    })

    total_biomass_reaction = cobra.Reaction("Total_biomass")

    total_biomass_reaction.add_metabolites({
        luciana_diel_model.metabolites.get_by_id('Leaf_biomass'): -0.39,
        luciana_diel_model.metabolites.get_by_id('Phellogen_biomass'): -0.12,
        luciana_diel_model.metabolites.get_by_id('Ibark_biomass'): -0.49,
        luciana_diel_model.metabolites.get_by_id('Total_biomass'): 1.0,
    })

    EX_total_biomass_reaction = cobra.Reaction("EX_Total_biomass")

    EX_total_biomass_reaction.add_metabolites({
        luciana_diel_model.metabolites.get_by_id('Total_biomass'): -1.0
    })

    EX_Leaf_reaction = cobra.Reaction("EX_Leaf")

    EX_Leaf_reaction.add_metabolites({
        luciana_diel_model.metabolites.get_by_id('Leaf_biomass'): -1.0
    })

    EX_Phellogen_reaction = cobra.Reaction("EX_Phellogen")

    EX_Phellogen_reaction.add_metabolites({
        luciana_diel_model.metabolites.get_by_id('Phellogen_biomass'): -1.0
    })

    EX_Ibark_reaction = cobra.Reaction("EX_Ibark")

    EX_Ibark_reaction.add_metabolites({
        luciana_diel_model.metabolites.get_by_id('Ibark_biomass'): -1.0
    })

    luciana_diel_model.add_reactions([leaf_biomass_reaction, phellogen_biomass_reaction, ibark_biomass_reaction,
                                      total_biomass_reaction, EX_total_biomass_reaction, EX_Leaf_reaction,
                                      EX_Phellogen_reaction, EX_Ibark_reaction])

    luciana_diel_model.objective = 'Total_biomass'
    luciana_diel_model.objective_direction = 'max'

    cobra.io.write_sbml_model(luciana_diel_model, "quercus/(changed)diel_multi_quercus_model.xml")