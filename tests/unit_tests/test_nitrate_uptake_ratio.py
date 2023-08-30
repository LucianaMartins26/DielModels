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

        nitrate_uptake_ratio_calibrator = NitrateUptakeRatioCalibrator(diel_model_copy, ["Ex4_Day"], ["Ex4_Night"])
        nitrate_uptake_ratio_calibrator.ratio_set()

        nitrate_uptake_reaction_day = diel_model_copy.reactions.get_by_id("Ex4_Day")
        nitrate_uptake_reaction_night = diel_model_copy.reactions.get_by_id("Ex4_Night")

        solution = pfba(diel_model_copy).fluxes

        self.assertEqual(round(solution[nitrate_uptake_reaction_day.id] * 2, 4),
                         round(solution[nitrate_uptake_reaction_night.id] * 3, 4))

    def test_ratio_set_with_invalid_day_reaction(self):

        diel_model = os.path.join(TEST_DIR, "data", "Diel_Model_AraGEM_with_biomass_total.xml")
        diel_model_2 = cobra.io.read_sbml_model(diel_model)
        diel_model_copy = copy.deepcopy(diel_model_2)

        nitrate_uptake_ratio_calibrator = NitrateUptakeRatioCalibrator(diel_model_copy, ["Invalid"], ["Ex4_Night"])

        with self.assertRaises(ValueError):
            nitrate_uptake_ratio_calibrator.ratio_set()

    def test_ratio_set_with_invalid_night_reaction(self):

        diel_model = os.path.join(TEST_DIR, "data", "Diel_Model_AraGEM_with_biomass_total.xml")
        diel_model_2 = cobra.io.read_sbml_model(diel_model)
        diel_model_copy = copy.deepcopy(diel_model_2)

        nitrate_uptake_ratio_calibrator = NitrateUptakeRatioCalibrator(diel_model_copy, ["Ex4_Day"], ["Invalid"])

        with self.assertRaises(ValueError):
            nitrate_uptake_ratio_calibrator.ratio_set()

    def test_ratio_set_multi_tissue(self):
        diel_multi_tissue_model = os.path.join(TEST_DIR, "data", "Diel_Multi_Tissue_with_biomass_total.xml")
        multi_model = cobra.io.read_sbml_model(diel_multi_tissue_model)
        multi_model_copy = copy.deepcopy(multi_model)

        multi_model_copy.reactions.get_by_id("ExMe5_Day").bounds = (0, 1000)
        multi_model_copy.reactions.get_by_id("ExMe5_Night").bounds = (0, 1000)
        multi_model_copy.reactions.get_by_id("ExBe5_Day").bounds = (0, 1000)
        multi_model_copy.reactions.get_by_id("ExBe5_Night").bounds = (0, 1000)

        nitrate_uptake_ratio_calibrator = NitrateUptakeRatioCalibrator(multi_model_copy, ["ExBe10_Day"], ["ExBe10_Night"])
        nitrate_uptake_ratio_calibrator.ratio_set()

        for nitrate_uptake_reaction_day, nitrate_uptake_reaction_night in zip(["ExBe10_Day"], ["ExBe10_Night"]):
            nitrate_reaction_day = multi_model_copy.reactions.get_by_id(nitrate_uptake_reaction_day)
            nitrate_reaction_night = multi_model_copy.reactions.get_by_id(nitrate_uptake_reaction_night)

            solution = pfba(multi_model_copy).fluxes

            self.assertEqual(round(solution[nitrate_reaction_day.id] * 2, 4),
                             round(solution[nitrate_reaction_night.id] * 3, 4))

    def test_ratio_set_with_invalid_day_reaction_multi_tissue(self):
        diel_multi_tissue_model = os.path.join(TEST_DIR, "data", "Diel_Multi_Tissue_with_biomass_total.xml")
        multi_model = cobra.io.read_sbml_model(diel_multi_tissue_model)
        multi_model_copy = copy.deepcopy(multi_model)

        nitrate_uptake_ratio_calibrator = NitrateUptakeRatioCalibrator(multi_model_copy, ["Invalid"], ["ExBe10_Night"])

        with self.assertRaises(ValueError):
            nitrate_uptake_ratio_calibrator.ratio_set()

    def test_ratio_set_with_invalid_night_reaction_multi_tissue(self):
        diel_multi_tissue_model = os.path.join(TEST_DIR, "data", "Diel_Multi_Tissue_with_biomass_total.xml")
        multi_model = cobra.io.read_sbml_model(diel_multi_tissue_model)
        multi_model_copy = copy.deepcopy(multi_model)

        nitrate_uptake_ratio_calibrator = NitrateUptakeRatioCalibrator(multi_model_copy, ["ExBe10_Day"], ["Invalid"])

        with self.assertRaises(ValueError):
            nitrate_uptake_ratio_calibrator.ratio_set()
