import os
import copy
from unittest import TestCase

import cobra

from diel_models.nitrate_uptake_ratio import NitrateUptakeRatioCalibrator
from tests import TEST_DIR


class TestNitrateUptakeRatioCalibrator(TestCase):

    def test_ratio_set(self):

        diel_model = os.path.join(TEST_DIR, "data", "Diel_Model_AraGEM_with_biomass_total.xml")
        diel_model_2 = cobra.io.read_sbml_model(diel_model)
        diel_model_copy = copy.deepcopy(diel_model_2)

        nitrateuptakeratiocalibrator = NitrateUptakeRatioCalibrator(diel_model_copy, "Ex4_Day", "Ex4_Night")
        nitrateuptakeratiocalibrator.ratio_set()

        nitrate_uptake_reaction_day = diel_model_copy.reactions.get_by_id("Ex4_Day")
        nitrate_uptake_reaction_night = diel_model_copy.reactions.get_by_id("Ex4_Night")

        for metabolite_id, coefficient in nitrate_uptake_reaction_day.metabolites.items():
            self.assertEqual(coefficient, 3.0)

        for metabolite_id, coefficient in nitrate_uptake_reaction_night.metabolites.items():
            self.assertEqual(coefficient, 2.0)

    def test_ratio_set_with_invalid_day_reaction(self):

        diel_model = os.path.join(TEST_DIR, "data", "Diel_Model_AraGEM_with_biomass_total.xml")
        diel_model_2 = cobra.io.read_sbml_model(diel_model)
        diel_model_copy = copy.deepcopy(diel_model_2)

        nitrateuptakeratiocalibrator = NitrateUptakeRatioCalibrator(diel_model_copy, "Invalid", "Ex4_Night")

        with self.assertRaises(ValueError):
            nitrateuptakeratiocalibrator.ratio_set()

    def test_ratio_set_with_invalid_night_reaction(self):

        diel_model = os.path.join(TEST_DIR, "data", "Diel_Model_AraGEM_with_biomass_total.xml")
        diel_model_2 = cobra.io.read_sbml_model(diel_model)
        diel_model_copy = copy.deepcopy(diel_model_2)

        nitrateuptakeratiocalibrator = NitrateUptakeRatioCalibrator(diel_model_copy, "Ex4_Day", "Invalid")

        with self.assertRaises(ValueError):
            nitrateuptakeratiocalibrator.ratio_set()
