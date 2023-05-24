import cobra
from cobra import Model
from abc import ABC, abstractmethod


class Step(ABC):
    @abstractmethod
    def run(self) -> None:
        """Performs the step."""
        pass

    def validate(self) -> None:
        """Validates the model of the step."""
        pass


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
        It runs the validate method followed by the run method.
        The resulting model is then set as self.model to be used in the next step.
        """

        for step in self.steps:
            step.validate()
            self.model = step.run()
