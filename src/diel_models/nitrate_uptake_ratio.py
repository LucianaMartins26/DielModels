from cobra import Model


class RatioUptakeNitrateCalibrator:

    def __init__(self, model: Model, id_nitrate_uptake_reaction_day: str,
                 id_nitrate_uptake_reaction_night: str) -> None:
        """
        Parameters
        ----------
        model: cobra.Model
            Metabolic model
        id_nitrate_uptake_reaction_day: string
            Identification of day nitrate uptake reaction.
        id_nitrate_uptake_reaction_night: string
            Identification of night nitrate uptake reaction.
        """
        self.model: Model = model
        self.id_nitrate_uptake_reaction_day: str = id_nitrate_uptake_reaction_day
        self.id_nitrate_uptake_reaction_night: str = id_nitrate_uptake_reaction_night

    def ratio_set(self) -> None:
        """
        This function establishes a 3:2 ratio of nitrate uptake between day and night, respectively.
        """
        if self.model.reactions.has_id(self.id_nitrate_uptake_reaction_day):
            nitrate_uptake_reaction_day = self.model.reactions.get_by_id(self.id_nitrate_uptake_reaction_day)
        else:
            raise ValueError("id_nitrate_uptake_reaction_day not present in the model that was given.")

        if self.model.reactions.has_id(self.id_nitrate_uptake_reaction_night):
            nitrate_uptake_reaction_night = self.model.reactions.get_by_id(self.id_nitrate_uptake_reaction_night)
        else:
            raise ValueError("id_nitrate_uptake_reaction_night not present in the model that was given.")

        for metabolite_id in nitrate_uptake_reaction_day.metabolites:
            nitrate_uptake_reaction_day.add_metabolites(
                {metabolite_id: -nitrate_uptake_reaction_day.metabolites[metabolite_id]})
            nitrate_uptake_reaction_day.add_metabolites({metabolite_id: 3.0})

        for metabolite_id in nitrate_uptake_reaction_night.metabolites:
            nitrate_uptake_reaction_night.add_metabolites(
                {metabolite_id: -nitrate_uptake_reaction_night.metabolites[metabolite_id]})
            nitrate_uptake_reaction_night.add_metabolites({metabolite_id: 2.0})
