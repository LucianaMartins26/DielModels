from cobra import Model, Reaction
from diel_models.pipeline import Step


class BiomassAdjuster(Step):

    def __init__(self, model: Model, id_biomass_reaction_day: str, id_biomass_reaction_night: str) -> None:
        """
        Parameters
        ----------
        model: cobra.Model
            Metabolic model
        id_biomass_reaction_day: string
            Identification of the biomass reaction at night
        id_biomass_reaction_night: string
            Identification of the biomass reaction at day
        """

        self.model: Model = model
        self.id_biomass_reaction_day: str = id_biomass_reaction_day
        self.id_biomass_reaction_night: str = id_biomass_reaction_night

    def total_biomass_reaction(self) -> None:
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
                biomass_reaction_total.add_metabolites({metabolite: coefficient / 2})

        self.model.add_reactions([biomass_reaction_total])
        self.model.objective = biomass_reaction_total
        biomass_reaction_day.bounds = (0, 0)
        biomass_reaction_night.bounds = (0, 0)

    def run(self) -> Model:
        """
        Executes the methods of the class BiomassRegulator

        Returns
        Model
        """
        self.total_biomass_reaction()

        return self.model

    def validate(self) -> None:
        pass
