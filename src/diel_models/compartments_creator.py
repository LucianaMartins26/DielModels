import copy
from cobra import Model, Reaction


class CompartmentsCreator:

    def __init__(self, model: Model) -> None:
        """
        Constructor

        Parameters
        ----------
        model: cobra.Model
            The metabolic model
        """
        self.model: Model = model

    def day_attribution(self) -> Model:
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

        return self.model.metabolites

    def duplicate(self) -> Model:
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
                    duplicate_reaction.add_metabolites({duplicate_metabolite: model_reaction.metabolites[model_metabolite]})

                if not self.model.reactions.has_id(duplicate_reaction.id):
                    self.model.add_reactions([duplicate_reaction])

        for compartment_id, compartment_description in compartments_copy.items():
            self.model._compartments[compartment_id.replace("_Day", "_Night")] = compartment_description.replace("Day", "Night")

        return self.model
