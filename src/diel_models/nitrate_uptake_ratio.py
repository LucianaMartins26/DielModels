from typing import List

from cobra import Model
from diel_models.pipeline import Step


class NitrateUptakeRatioCalibrator(Step):

    def __init__(self, model: Model, id_nitrate_uptake_reaction_day: List[str],
                 id_nitrate_uptake_reaction_night: List[str], day_ratio_value: int = 3, night_ratio_value: int = 2) -> None:
        """
        Constructor

        Parameters
        ----------
        model: cobra.Model
            Metabolic model
        id_nitrate_uptake_reaction_day: List[str]
            Identification of day nitrate uptake reaction(s) - in case of for example, multi tissue models.
        id_nitrate_uptake_reaction_night: List[str]
            Identification of night nitrate uptake reaction(s) - in case of for example, multi tissue models.
        day_ratio_value: int, optional
            The ratio of nitrate uptake during the day, default is 3.
        night_ratio_value: int, optional
            The ratio of nitrate uptake during the night, default is 2.
        """
        self.model: Model = model
        self.id_nitrate_uptake_reaction_day: List[str] = id_nitrate_uptake_reaction_day
        self.id_nitrate_uptake_reaction_night: List[str] = id_nitrate_uptake_reaction_night
        self.day_ratio_value: int = day_ratio_value
        self.night_ratio_value: int = night_ratio_value

    def ratio_set(self) -> None:
        """
        This function establishes a 3:2 ratio (by default) of nitrate uptake between day and night, respectively.
        The ratio can be changed.

        Raises:
            ValueError: If the nitrate uptake reaction ID is not present in the given model.
        """
        for nitrate_uptake_day_reaction, nitrate_uptake_night_reaction in \
                zip(self.id_nitrate_uptake_reaction_day, self.id_nitrate_uptake_reaction_night):
            if self.model.reactions.has_id(nitrate_uptake_day_reaction) and \
                    self.model.reactions.has_id(nitrate_uptake_night_reaction):
                nitrate_uptake_reaction_day = self.model.reactions.get_by_id(nitrate_uptake_day_reaction)
                nitrate_uptake_reaction_night = self.model.reactions.get_by_id(nitrate_uptake_night_reaction)

                same_flux = self.model.problem.Constraint(
                    nitrate_uptake_reaction_day.flux_expression * self.night_ratio_value -
                    nitrate_uptake_reaction_night.flux_expression * self.day_ratio_value, lb=0, ub=0)
                self.model.add_cons_vars(same_flux)

            else:
                raise ValueError("id_nitrate_uptake_reaction not present in the model that was given.")

    def run(self) -> Model:
        """
        Executes the method of the class NitrateUptakeRatioCalibrator.
        """
        self.ratio_set()

        return self.model

    def validate(self) -> None:
        pass