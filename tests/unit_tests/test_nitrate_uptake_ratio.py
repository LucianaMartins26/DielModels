import os
import copy
from unittest import TestCase

import cobra

from cobra.flux_analysis import pfba

from diel_models.nitrate_uptake_ratio import NitrateUptakeRatioCalibrator
from tests import TEST_DIR


class TestNitrateUptakeRatioCalibrator(TestCase):

    def test_ratio_set(self):

        diel_model = os.path.join(TEST_DIR, "data", "Diel_Model_AraGEM_with_biomass_total.xml")
        diel_model_2 = cobra.io.read_sbml_model(diel_model)
        diel_model_copy = copy.deepcopy(diel_model_2)

        diel_model_copy.reactions.get_by_id("Ex5_Night").bounds = (0, 1000)
        diel_model_copy.reactions.get_by_id("Ex5_Day").bounds = (0, 1000)

        nitrateuptakeratiocalibrator = NitrateUptakeRatioCalibrator(diel_model_copy, "Ex4_Day", "Ex4_Night")
        nitrateuptakeratiocalibrator.ratio_set()

        nitrate_uptake_reaction_day = diel_model_copy.reactions.get_by_id("Ex4_Day")
        nitrate_uptake_reaction_night = diel_model_copy.reactions.get_by_id("Ex4_Night")

        solution = pfba(diel_model_copy).fluxes

        self.assertEqual(round(solution[nitrate_uptake_reaction_day.id] * 2, 4),
                         round(solution[nitrate_uptake_reaction_night.id] * 3, 4))

    def test_ratio_set_with_invalid_day_reaction(self):

        diel_model = os.path.join(TEST_DIR, "data", "Diel_Model_AraGEM_with_biomass_total.xml")
        diel_model_2 = cobra.io.read_sbml_model(diel_model)
        diel_model_copy = copy.deepcopy(diel_model_2)

        nitrate_uptake_ratio_calibrator = NitrateUptakeRatioCalibrator(diel_model_copy, "Invalid", "Ex4_Night")

        with self.assertRaises(ValueError):
            nitrate_uptake_ratio_calibrator.ratio_set()

    def test_ratio_set_with_invalid_night_reaction(self):

        diel_model = os.path.join(TEST_DIR, "data", "Diel_Model_AraGEM_with_biomass_total.xml")
        diel_model_2 = cobra.io.read_sbml_model(diel_model)
        diel_model_copy = copy.deepcopy(diel_model_2)

        nitrate_uptake_ratio_calibrator = NitrateUptakeRatioCalibrator(diel_model_copy, "Ex4_Day", "Invalid")

        with self.assertRaises(ValueError):
            nitrate_uptake_ratio_calibrator.ratio_set()
