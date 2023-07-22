from typing import List

from cobra import Model
from diel_models.pipeline import Step


class NitrateUptakeRatioCalibrator(Step):

    def __init__(self, model: Model, id_nitrate_uptake_reaction_day: List[str],
                 id_nitrate_uptake_reaction_night: List[str]) -> None:
        """
        Parameters
        ----------
        model: cobra.Model
            Metabolic model
        id_nitrate_uptake_reaction_day: List[str]
            Identification of day nitrate uptake reaction(s) - in case of for example, multi tissue models.
        id_nitrate_uptake_reaction_night: List[str]
            Identification of night nitrate uptake reaction(s) - in case of for example, multi tissue models.
        """
        self.model: Model = model
        self.id_nitrate_uptake_reaction_day: List[str] = id_nitrate_uptake_reaction_day
        self.id_nitrate_uptake_reaction_night: List[str] = id_nitrate_uptake_reaction_night

    def ratio_set(self) -> None:
        """
        This function establishes a 3:2 ratio of nitrate uptake between day and night, respectively.
        """
        for nitrate_uptake_day_reaction, nitrate_uptake_night_reaction in \
                zip(self.id_nitrate_uptake_reaction_day, self.id_nitrate_uptake_reaction_night):
            if self.model.reactions.has_id(nitrate_uptake_day_reaction) and \
                    self.model.reactions.has_id(nitrate_uptake_night_reaction):
                nitrate_uptake_reaction_day = self.model.reactions.get_by_id(nitrate_uptake_day_reaction)
                nitrate_uptake_reaction_night = self.model.reactions.get_by_id(nitrate_uptake_night_reaction)

                same_flux = self.model.problem.Constraint(
                    nitrate_uptake_reaction_day.flux_expression * 2 -
                    nitrate_uptake_reaction_night.flux_expression * 3, lb=0, ub=0)
                self.model.add_cons_vars(same_flux)

            else:
                raise ValueError("id_nitrate_uptake_reaction not present in the model that was given.")

    def run(self) -> Model:
        """
        Executes the method of the class NitrateUptakeRatioCalibrator

        Returns
        Model
        """
        self.ratio_set()

        return self.model

    def validate(self) -> None:
        pass