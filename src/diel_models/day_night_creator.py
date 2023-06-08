import copy
from cobra import Model, Reaction
from diel_models.pipeline import Step


class DayNightCreator(Step):

    def __init__(self, model: Model) -> None:
        """
        Constructor

        Parameters
        ----------
        model: cobra.Model
            Metabolic model
        """
        self.model: Model = model

    def day_attribution(self) -> None:
        """
        Loop into the reactions and metabolites of a metabolic model
        Returns
        -------
        Reactions and metabolites ids with "_Day" as sufix
        """
        compartments_copy = copy.deepcopy(self.model.compartments)
        for model_reaction in self.model.reactions:
            model_reaction.id = model_reaction.id + "_Day"
        for model_metabolite in self.model.metabolites:
            model_metabolite.id = model_metabolite.id + "_Day"
            model_metabolite.name = model_metabolite.name + " Day"
            model_metabolite.compartment = model_metabolite.compartment + "_Day"

        for compartment_id, compartment_description in compartments_copy.items():
            self.model._compartments[compartment_id + "_Day"] = compartment_description + " Day"

    def duplicate(self) -> None:
        """
        Function that duplicates the original reactions and replaces
        the suffix "_Day" with the suffix "_Night" and further duplicates
        the corresponding metabolites

        Returns
        -------
        The model with the reactions and the metabolites duplicated and properly identified
        """
        compartments_copy = copy.deepcopy(self.model.compartments)
        for model_reaction in self.model.reactions:
            if not model_reaction.id.endswith("_Night"):
                duplicate_reaction = Reaction(id=model_reaction.id.replace("_Day", "_Night"),
                                              name=model_reaction.name,
                                              subsystem=model_reaction.subsystem,
                                              lower_bound=model_reaction.lower_bound,
                                              upper_bound=model_reaction.upper_bound)

                for model_metabolite in model_reaction.metabolites:
                    duplicate_metabolite = model_metabolite.copy()
                    duplicate_metabolite.id = model_metabolite.id.replace("_Day", "_Night")
                    duplicate_metabolite.name = model_metabolite.name.replace("Day", "Night")
                    duplicate_metabolite.compartment = model_metabolite.compartment.replace("_Day", "_Night")
                    duplicate_reaction.add_metabolites(
                        {duplicate_metabolite: model_reaction.metabolites[model_metabolite]})

                if not self.model.reactions.has_id(duplicate_reaction.id):
                    self.model.add_reactions([duplicate_reaction])

        for compartment_id, compartment_description in compartments_copy.items():
            self.model._compartments[compartment_id.replace("_Day", "_Night")] = compartment_description.replace("Day",
                                                                                                                 "Night")

    def run(self) -> Model:
        """
        Executes the methods of the class DayNightCreator

        Returns
        Model
        """
        self.day_attribution()
        self.duplicate()

        return self.model

    def validate(self) -> None:
        """
        Validates the model received initially in terms of reactions, metabolites and objective function
        """

        assert len(self.model.reactions) > 0, "The model does not have any reaction."
        assert len(self.model.metabolites) > 0, "The model does not have any metabolite."
        assert self.model.objective is not None, "The model does not have any objective function defined."
