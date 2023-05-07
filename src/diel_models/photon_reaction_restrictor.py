from cobra import Model


class PhotonReactionRestrictor:

    def __init__(self, model: Model, id_photon_reaction_night: str) -> None:
        self.model: Model = model
        self.id_photon_reaction_night: str = id_photon_reaction_night

    def restrain(self) -> None:
        photon_reaction_night = self.model.reactions.get_by_id(self.id_photon_reaction_night)
        photon_reaction_night.lower_bound = 0
        photon_reaction_night.upper_bound = 0
