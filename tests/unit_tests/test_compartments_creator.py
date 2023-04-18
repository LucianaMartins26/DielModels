import copy
import os
from unittest import TestCase

import cobra

from diel_models.compartments_creator import CompartmentsCreator
from tests import TEST_DIR


class TestCompartmentsCreator(TestCase):

    def test_compartments_creator(self):

        ara_gem_model = os.path.join(TEST_DIR, "data", "AraGEM2010.xml")
        non_diel_model = cobra.io.read_sbml_model(ara_gem_model)
        non_diel_model_copy = copy.deepcopy(non_diel_model)

        compartment_creator = CompartmentsCreator(non_diel_model_copy)

        compartment_creator.day_attribution()
        for reaction in non_diel_model_copy.reactions:
            self.assertIn("_Day", reaction.id)

        for metabolite in non_diel_model_copy.metabolites:
            self.assertIn("_Day", metabolite.id)

        for compartment in non_diel_model_copy.compartments:
            self.assertIn("_Day", compartment)

        cobra.io.write_sbml_model(non_diel_model_copy, os.path.join(TEST_DIR, "data", "AraGEM_day.xml"))

    def test_duplicate_models_day(self):

        ara_gem_day = cobra.io.read_sbml_model(os.path.join(TEST_DIR, "data", "AraGEM_day.xml"))

        compartment_creator = CompartmentsCreator(ara_gem_day)
        compartment_creator.duplicate()

        for reaction in ara_gem_day.reactions:
            assert "_Day" in reaction.id or "_Night" in reaction.id

        for metabolite in ara_gem_day.metabolites:
            assert "_Day" in metabolite.id or "_Night" in metabolite.id

        for compartment in ara_gem_day.compartments:
            assert "_Day" in compartment or "_Night" in compartment

        cobra.io.write_sbml_model(ara_gem_day, os.path.join(TEST_DIR, "data", "AraGEM_day_night.xml"))