import cobra
from cobra import Model


class Pipeline:
    def __init__(self, model: Model, steps: list) -> None:
        """
        Parameters
        ----------
        model: cobra.Model
            Metabolic model
        steps: list
            All stages to be run by the pipeline
        """

        self.steps = steps
        self.model = model

    def run(self) -> None:
        """
        It runs the validate method followed by the run method and writes the resulting xml model from each step.
        The resulting model is then set as self.model to be used in the next step.
        """

        for step in self.steps:
            step.validate()
            step.run()
            cobra.io.write_sbml_model(self.model, "Model.xml")
            self.model = cobra.io.read_sbml_model("Model.xml")
