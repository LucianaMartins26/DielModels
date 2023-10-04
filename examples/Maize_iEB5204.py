import cobra
import os
from tests import TEST_DIR
from diel_models.diel_models_creator import diel_models_creator

def diel_maize_iEB5204(model):

    biomass_reactions = set()

    for met in model.metabolites:
        if 'biomass' in met.name:
            biomass_reactions.update(met.reactions)

    biomass_rxn = cobra.Reaction("Biomass_rxn")
    biomass_rxn.name = "Biomass reaction"

    for rxn in biomass_reactions:
        individual_rxn = model.reactions.get_by_id(rxn.id)
        biomass_rxn.add_metabolites(
            {metabolito: -coeficiente for metabolito, coeficiente in individual_rxn.metabolites.items()})
        individual_rxn.knock_out()

    model.add_reactions([biomass_rxn])

    model.objective = model.reactions.get_by_id("tx__Light_")

    diel_models_creator(model,
                        ["SUCROSE", "SULFATE", "NITRATE", "HIS", "ILE", "LEU", "LYS", "MET", "PHE", "TRP", "THR", "VAL",
                         "ASN", "CYS", "GLN", "GLY", "PRO", "TYR", "GLT", "L_alanine", "L_ASPARTATE", "SER",
                         "starch_monomer_equivalent", "BETA_D_FRUCTOSE", "MAL", "FUM", "CIT"], ["tx__Light_"],
                        "Biomass_rxn", ["tx_NITRATE"])

    cobra.io.write_sbml_model(model, os.path.join(TEST_DIR, 'models', 'diel_maizeiEB5204_model.xml'))


if __name__ == '__main__':
    maizeiEB5204_model_path = os.path.join(TEST_DIR, 'models', 'Maize_iEB5204.xml')
    maizeiEB5204_model = cobra.io.read_sbml_model(maizeiEB5204_model_path)
    diel_maize_iEB5204(maizeiEB5204_model)