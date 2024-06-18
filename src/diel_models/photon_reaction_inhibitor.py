from typing import List

from cobra import Model
from diel_models.pipeline import Step


class PhotonReactionInhibitor(Step):

    def __init__(self, model: Model, id_photon_reaction_night: List[str]) -> None:
        """
        Constructor

        Parameters
        ----------
        model: cobra.Model
            Metabolic model
        id_photon_reaction_night: List[str]
            Identification of the photon reaction(s) at night - in case of, for example, multi tissue models.
        """
        self.model: Model = model
        self.id_photon_reaction_night: List[str] = id_photon_reaction_night

    def restrain(self) -> None:
        """
        Function that resets the photon reaction(s) limits to zero at night.

        Raises:
            ValueError: If the photon uptake reaction ID is not present in the given model.
        """

        for photon_night_reaction in self.id_photon_reaction_night:
            if self.model.reactions.has_id(photon_night_reaction):
                photon_reaction_night = self.model.reactions.get_by_id(photon_night_reaction)
                photon_reaction_night.bounds = (0, 0)
            else:
                raise ValueError("Reaction id not present in the model that was given.")

    def run(self) -> Model:
        """
        Executes the method of the class PhotonReactionInhibitor.
        """
        self.restrain()

        return self.model

    def validate(self) -> None:
        """
        Validates the model that, in addition to the above factors, it must contain metabolites and storage pool
        compartments.
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
