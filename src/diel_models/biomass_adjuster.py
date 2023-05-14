from cobra import Model, Reaction
from typing import List


class BiomassAdjuster:

    def __init__(self, model: Model, id_biomass_reaction_day: str, id_biomass_reaction_night: str,
                 photosynthesis_reactions_at_night: List[str]) -> None:
        """
        Parameters
        ----------
        model: cobra.Model
            Metabolic model
        id_biomass_reaction_day: string
            Identification of the biomass reaction at night
        id_biomass_reaction_night: string
            Identification of the biomass reaction at day
        photosynthesis_reactions_at_night: List of strings
            List with identifications of the reactions of chlorophylls, caretonoids and/or others
        """

        self.model: Model = model
        self.id_biomass_reaction_day: str = id_biomass_reaction_day
        self.id_biomass_reaction_night: str = id_biomass_reaction_night
        self.photosynthesis_reactions_at_night: List[str] = photosynthesis_reactions_at_night

    def reset_boundaries(self) -> None:
        """
        Function that zeroes in on the limits of the given reactions responsible
        for absorbing light and important for photosynthesis, since this process
        does not take place at night.
        """

        for photosynthesis_reaction in self.photosynthesis_reactions_at_night:
            if photosynthesis_reaction in self.model.reactions:
                self.model.reactions.get_by_id(photosynthesis_reaction).lower_bound = 0
                self.model.reactions.get_by_id(photosynthesis_reaction).upper_bound = 0
            else:
                raise ValueError("Reaction id not present in the model that was given.")

    def total_biomass_reaction(self) -> Reaction:
        """
        Function that joins the two biomass reactions (day and night) into one.
        Defines this new reaction as the objective function of the model.
        Returns
        -------
        biomass_reaction_total: cobra.Reaction
        """
        if self.model.reactions.has_id(self.id_biomass_reaction_day) and \
                self.model.reactions.has_id(self.id_biomass_reaction_night):
            biomass_reaction_day = self.model.reactions.get_by_id(self.id_biomass_reaction_day)
            biomass_reaction_night = self.model.reactions.get_by_id(self.id_biomass_reaction_night)

        else:
            raise ValueError("Reaction id not present in the model that was given")

        biomass_reaction_total = Reaction(id="Biomass_Total",
                                          name="Total Biomass Reaction",
                                          subsystem='',
                                          lower_bound=0,
                                          upper_bound=1000)

        for reaction in [biomass_reaction_day, biomass_reaction_night]:
            for metabolite in reaction.metabolites:
                coefficient = reaction.get_coefficient(metabolite.id)
                biomass_reaction_total.add_metabolites({metabolite: coefficient})

        self.model.add_reactions([biomass_reaction_total])
        self.model.objective = biomass_reaction_total

        return biomass_reaction_total
