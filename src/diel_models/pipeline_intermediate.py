from cobra import Model
from typing import List
from abc import ABC, abstractmethod
from diel_models.compartments_creator import CompartmentsCreator
from diel_models.storage_pool_creator import StoragePoolCreator
from diel_models.photon_reaction_restrictor import PhotonReactionRestrictor
from diel_models.biomass_adjuster import BiomassAdjuster
from diel_models.nitrate_uptake_ratio import RatioUptakeNitrateCalibrator


class Step(ABC):
    @abstractmethod
    def run(self) -> None:
        """Performs the step."""
        pass

    def validate(self) -> None:
        """Validates the model of the step."""
        pass


class DayNightCreator(Step):

    def __init__(self, model: Model) -> None:
        """
        Parameters
        ----------
        model: cobra.Model
            Metabolic model
        """

        self.model = model

    def run(self) -> None:
        """
        Executes the methods of the class CompartmentsCreator
        """

        test = CompartmentsCreator(self.model)
        test.day_attribution()
        test.duplicate()

    def validate(self) -> None:
        """
        Validates the model received initially in terms of reactions, metabolites and objective function
        """

        assert len(self.model.reactions) > 0, "The model does not have any reaction."
        assert len(self.model.metabolites) > 0, "The model does not have any metabolite."
        assert self.model.objective is not None, "The model does not have any objective function defined."


class StoragePoolGenerator(Step):

    def __init__(self, model: Model, metabolites: List[str]) -> None:
        """
        Parameters
        ----------
        model: cobra.Model
            Metabolite Model
        metabolites: List[str]
            List with ids of metabolites to be placed in the storage pool
        """

        self.model = model
        self.metabolites = metabolites

    def run(self) -> None:
        """
        Executes the methods of the class StoragePoolCreator
        """

        test = StoragePoolCreator(self.model, self.metabolites)
        test.create_storage_pool_metabolites()
        test.create_storage_pool_first_reactions()
        test.create_storage_pool_second_reactions()

    def validate(self) -> None:
        """
        Validates the model, since it has to have metabolites, reactions and a Day and Night compartments
        """

        for reaction in self.model.reactions:
            assert "_Day" in reaction.id or "_Night" in reaction.id, "The model does not have Day and Night reactions."
        for metabolite in self.model.metabolites:
            assert "_Day" in metabolite.id or "_Night" in metabolite.id, "The model does not have Day and Night " \
                                                                         "metabolites."
        for compartment in self.model.compartments:
            assert "_Day" in compartment or "_Night" in compartment, "The model does not have Day and Night " \
                                                                     "compartments."


class PhotonReactionInhibitor(Step):

    def __init__(self, model: Model, id_photon_reaction_night: str) -> None:
        """
        Parameters
        ----------
        model: cobra.Model
            Metabolic Model
        id_photon_reaction_night: str
            Identification of the photon reaction at night.
        """

        self.model: Model = model
        self.id_photon_reaction_night: str = id_photon_reaction_night

    def run(self) -> None:
        """
        Executes the method of the class PhotonReactionRestrictor
        """

        test = PhotonReactionRestrictor(self.model, self.id_photon_reaction_night)
        test.restrain()

    def validate(self) -> None:
        """
        Validates the model that in addition to the above factors it must contain metabolites and storage pool
        compartments
        """

        for compartment in self.model.compartments:
            assert "_Day" in compartment or "_Night" in compartment or 'sp' in compartment, "The model does not have " \
                                                                                            "storage pool compartment"

        for metabolite in self.model.metabolites:
            if metabolite.compartment == "sp":
                assert "_sp" in metabolite.id, "The storage pool metabolites does not have sp suffix in their id"
                assert "Day" not in metabolite.name or "Night" not in metabolite.name, "The storage pool metabolites " \
                                                                                       "continue to have Day or Night" \
                                                                                       " in their name"


class BiomassRegulator(Step):

    def __init__(self, model: Model, id_biomass_reaction_day: str, id_biomass_reaction_night: str,
                 photosynthesis_reactions_at_night: List[str]) -> None:
        """
        Parameters
        ----------
        model: cobra.Model
            Metabolic Model
        id_biomass_reaction_day: str
            Identification of biomass reaction at day
        id_biomass_reaction_night: str
            Identification of biomass reaction at night
        photosynthesis_reactions_at_night: List[str]
            List with identifications of the reactions of chlorophylls, caretonoids and/or others
        """

        self.model: Model = model
        self.id_biomass_reaction_day: str = id_biomass_reaction_day
        self.id_biomass_reaction_night: str = id_biomass_reaction_night
        self.photosynthesis_reactions_at_night: List[str] = photosynthesis_reactions_at_night

    def run(self) -> None:
        """
        Executes the methods of the class BiomassAdjuster
        """

        test = BiomassAdjuster(self.model, self.id_biomass_reaction_day, self.id_biomass_reaction_night,
                               self.photosynthesis_reactions_at_night)
        test.reset_boundaries()
        test.total_biomass_reaction()

    def validate(self) -> None:
        pass


class NitrateUptakeRatioCalibrator(Step):

    def __init__(self, model: Model, id_nitrate_uptake_reaction_day: str,
                 id_nitrate_uptake_reaction_night: str) -> None:
        """
        Parameters
        ----------
        model: cobra.Model
            Metabolic model
        id_nitrate_uptake_reaction_day: str
            Identification of nitrate uptake reaction at day
        id_nitrate_uptake_reaction_night: str
            Identification of nitrate uptake reaction at night
        """

        self.model: Model = model
        self.id_nitrate_uptake_reaction_day: str = id_nitrate_uptake_reaction_day
        self.id_nitrate_uptake_reaction_night: str = id_nitrate_uptake_reaction_night

    def run(self) -> None:
        """
        Executes the method of the class RatioUptakeNitrateCalibrator
        """

        test = RatioUptakeNitrateCalibrator(self.model, self.id_nitrate_uptake_reaction_day,
                                            self.id_nitrate_uptake_reaction_night)
        test.ratio_set()

    def validate(self) -> None:
        pass
