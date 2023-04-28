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
        for m in self.model.metabolites:
            m.id = m.id + "_Day"
            m.name = m.name + " Day"
            m.compartment = m.compartment + "_Day"

        for k, v in compartments_copy.items():
            self.model._compartments[k + "_Day"] = v + " Day"

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
        for r in self.model.reactions:
            duplicate_r = Reaction(id=r.id.replace("_Day", "_Night"),
                                   name=r.name,
                                   subsystem=r.subsystem,
                                   lower_bound=r.lower_bound,
                                   upper_bound=r.upper_bound)

            for m in r.metabolites:
                duplicate_m = m.copy()
                duplicate_m.id = m.id.replace("_Day", "_Night")
                duplicate_m.name = m.name.replace("Day", "Night")
                duplicate_m.compartment = m.compartment.replace("_Day", "_Night")
                duplicate_r.add_metabolites({duplicate_m: r.metabolites[m]})

            self.model.add_reactions([duplicate_r])

        for k, v in compartments_copy.items():
            self.model._compartments[k.replace("_Day", "_Night")] = v.replace("Day", "Night")

        return self.model
