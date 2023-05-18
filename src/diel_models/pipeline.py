import cobra
from cobra import Model
from typing import List
from abc import ABC, abstractmethod
from diel_models.compartments_creator import CompartmentsCreator
from diel_models.storage_pool_creator import StoragePoolCreator
from diel_models.photon_reaction_restrictor import PhotonReactionRestrictor
from diel_models.biomass_adjuster import BiomassAdjuster


class Step(ABC):
    @abstractmethod
    def run(self):
        pass

    def validate(self):
        pass


class Compartments(Step):

    def __init__(self, model: Model):
        self.model = model

    def run(self):
        test = CompartmentsCreator(self.model)
        test.day_attribution()
        test.duplicate()

    def validate(self):
        assert len(self.model.reactions) > 0, "The model does not have any reaction."
        assert len(self.model.metabolites) > 0, "The model does not have any metabolite."
        assert self.model.objective is not None, "The model does not have any objective function defined."


class StoragePool(Step):

    def __init__(self, model: Model, metabolites: List[str]):
        self.model = model
        self.metabolites = metabolites

    def run(self):
        test = StoragePoolCreator(self.model, self.metabolites)
        test.create_storage_pool_metabolites()
        test.create_storage_pool_first_reactions()
        test.create_storage_pool_second_reactions()

    def validate(self):

        for reaction in self.model.reactions:
            assert "_Day" in reaction.id or "_Night" in reaction.id, "The model does not have Day and Night reactions."
        for metabolite in self.model.metabolites:
            assert "_Day" in metabolite.id or "_Night" in metabolite.id, "The model does not have Day and Night " \
                                                                         "metabolites."
        for compartment in self.model.compartments:
            assert "_Day" in compartment or "_Night" in compartment, "The model does not have Day and Night " \
                                                                     "compartments."


class PhotonRestrictor(Step):

    def __init__(self, model: Model, id_photon_reaction_night: str):
        self.model: Model = model
        self.id_photon_reaction_night: str = id_photon_reaction_night

    def run(self):
        test = PhotonReactionRestrictor(self.model, self.id_photon_reaction_night)
        test.restrain()

    def validate(self):

        for compartment in self.model.compartments:
            assert "_Day" in compartment or "_Night" in compartment or 'sp' in compartment, "The model does not have " \
                                                                                            "storage pool compartment"

        for metabolite in self.model.metabolites:
            if metabolite.compartment == "sp":
                assert "_sp" in metabolite.id, "The storage pool metabolites does not have sp suffix in their id"
                assert "Day" not in metabolite.name or "Night" not in metabolite.name, "The storage pool metabolites " \
                                                                                       "continue to have Day or Night" \
                                                                                       " in their name"


class Biomass(Step):

    def __init__(self, model: Model, id_biomass_reaction_day: str, id_biomass_reaction_night: str,
                 photosynthesis_reactions_at_night: List[str]):
        self.model: Model = model
        self.id_biomass_reaction_day: str = id_biomass_reaction_day
        self.id_biomass_reaction_night: str = id_biomass_reaction_night
        self.photosynthesis_reactions_at_night: List[str] = photosynthesis_reactions_at_night

    def run(self):
        test = BiomassAdjuster(self.model, self.id_biomass_reaction_day, self.id_biomass_reaction_night,
                               self.photosynthesis_reactions_at_night)
        test.reset_boundaries()
        test.total_biomass_reaction()

    def validate(self):
        pass


class Pipeline:
    def __init__(self, model: Model, steps):
        self.steps = steps
        self.model = model

    def run(self):
        for step in self.steps:
            step.validate()
            step.run()
            cobra.io.write_sbml_model(self.model, "Model.xml")
            self.model = cobra.io.read_sbml_model("Model.xml")
