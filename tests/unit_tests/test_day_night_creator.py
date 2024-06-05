import copy
import os
from unittest import TestCase

import cobra

from diel_models.day_night_creator import DayNightCreator
from tests import TEST_DIR


class TestDayNightCreator(TestCase):

    def test_compartments_creator(self):

        ara_gem_model = os.path.join(TEST_DIR, "data", "aragem_photo.xml")
        non_diel_model = cobra.io.read_sbml_model(ara_gem_model)
        non_diel_model_copy = copy.deepcopy(non_diel_model)

        compartment_creator = DayNightCreator(non_diel_model_copy)

        compartment_creator.day_attribution()
        for reaction in non_diel_model_copy.reactions:
            self.assertIn("_Day", reaction.id)

        for metabolite in non_diel_model_copy.metabolites:
            self.assertIn("_Day", metabolite.id)

        for compartment in non_diel_model_copy.compartments:
            self.assertIn("_Day", compartment)


    def test_duplicate(self):

        ara_gem_day = cobra.io.read_sbml_model(os.path.join(TEST_DIR, "data", "AraGEM_day.xml"))

        compartment_creator = DayNightCreator(ara_gem_day)
        compartment_creator.duplicate()

        for reaction in ara_gem_day.reactions:
            assert "_Day" in reaction.id or "_Night" in reaction.id

        for metabolite in ara_gem_day.metabolites:
            assert "_Day" in metabolite.id or "_Night" in metabolite.id

        for compartment in ara_gem_day.compartments:
            assert "_Day" in compartment or "_Night" in compartment


    def test_compartments_creator_multi_tissue(self):

        multi_tissue_model = os.path.join(TEST_DIR, "data", "TS4_Model_lv3.xml")
        multi_model = cobra.io.read_sbml_model(multi_tissue_model)
        multi_model_copy = copy.deepcopy(multi_model)

        compartment_creator = DayNightCreator(multi_model_copy)

        compartment_creator.day_attribution()
        for reaction in multi_model_copy.reactions:
            self.assertIn("_Day", reaction.id)

        for metabolite in multi_model_copy.metabolites:
            self.assertIn("_Day", metabolite.id)

        for compartment in multi_model_copy.compartments:
            self.assertIn("_Day", compartment)

    def test_duplicate_multi_tissue_model(self):

        multi_tissue_day = cobra.io.read_sbml_model(os.path.join(TEST_DIR, "data", "Multi_Tissue_day.xml"))

        compartment_creator = DayNightCreator(multi_tissue_day)
        compartment_creator.duplicate()

        for reaction in multi_tissue_day.reactions:
            assert "_Day" in reaction.id or "_Night" in reaction.id

        for metabolite in multi_tissue_day.metabolites:
            assert "_Day" in metabolite.id or "_Night" in metabolite.id

        for compartment in multi_tissue_day.compartments:
            assert "_Day" in compartment or "_Night" in compartment

    def test_compartments_creator_multi_tissue_quercus(self):

        multi_tissue_model = os.path.join(TEST_DIR, "models", "MultiTissueQuercusModel.xml")
        multi_model = cobra.io.read_sbml_model(multi_tissue_model)
        multi_model_copy = copy.deepcopy(multi_model)

        compartment_creator = DayNightCreator(multi_model_copy)

        compartment_creator.day_attribution()
        for reaction in multi_model_copy.reactions:
            self.assertIn("_Day", reaction.id)

        for metabolite in multi_model_copy.metabolites:
            self.assertIn("_Day", metabolite.id)

        for compartment in multi_model_copy.compartments:
            self.assertIn("_Day", compartment)

    def test_duplicate_multi_tissue_model_quercus(self):

        multi_tissue_day = cobra.io.read_sbml_model(os.path.join(TEST_DIR, "data", "Quercus_Multi_Tissue_Day.xml"))

        compartment_creator = DayNightCreator(multi_tissue_day)
        compartment_creator.duplicate()

        for reaction in multi_tissue_day.reactions:
            assert "_Day" in reaction.id or "_Night" in reaction.id

        for metabolite in multi_tissue_day.metabolites:
            assert "_Day" in metabolite.id or "_Night" in metabolite.id

        for compartment in multi_tissue_day.compartments:
            assert "_Day" in compartment or "_Night" in compartment

