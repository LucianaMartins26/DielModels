from cobra import Model


class PhotonReactionRestrictor:

    def __init__(self, model: Model, id_photon_reaction_night: str) -> None:
        """
        Parameters
        ----------
        model: cobra.Model
            Metabolic model
        id_photon_reaction_night: string
            Identification of the photon reaction at night.
        """
        self.model: Model = model
        self.id_photon_reaction_night: str = id_photon_reaction_night

    def restrain(self) -> None:
        """
        Function that resets the photon reaction limits to zero at night.
        """
        if self.model.reactions.has_id(self.id_photon_reaction_night):
            photon_reaction_night = self.model.reactions.get_by_id(self.id_photon_reaction_night)
            photon_reaction_night.bounds = (0, 0)
        else:
            raise ValueError("Reaction id not present in the model that was given.")
