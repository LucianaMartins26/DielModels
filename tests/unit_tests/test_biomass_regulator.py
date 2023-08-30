import os
import copy
from unittest import TestCase

import cobra

from diel_models.biomass_adjuster import BiomassAdjuster
from tests import TEST_DIR


class TestBiomassRegulator(TestCase):

    def test_total_biomass_reaction(self):
        diel_sp_no_night_photon_model = os.path.join(TEST_DIR, "data",
                                                     "Diel_AraGEM_sp_photon_restricted.xml")
        diel_model = cobra.io.read_sbml_model(diel_sp_no_night_photon_model)
        diel_model_copy = copy.deepcopy(diel_model)

        biomass_adjuster = BiomassAdjuster(diel_model_copy, "BIO_L_Day", "BIO_L_Night")
        biomass_adjuster.total_biomass_reaction()

        biomass_after = diel_model_copy.reactions.get_by_id("Biomass_Total")
        biomass_before = diel_model.reactions.get_by_id("BIO_L_Night")

        self.assertEqual(2 * (len(biomass_before.reactants)), len(biomass_after.reactants))
        self.assertEqual(2 * (len(biomass_before.products)), len(biomass_after.products))
        self.assertEqual(2 * (len(biomass_before.metabolites)), len(biomass_after.metabolites))

        self.assertIn('Biomass_Total', str(diel_model_copy.objective.expression))

    def test_total_biomass_with_invalid_biomass_reaction(self):
        diel_sp_no_night_photon_model = os.path.join(TEST_DIR, "data",
                                                     "Diel_AraGEM_sp_photon_restricted.xml")
        diel_model = cobra.io.read_sbml_model(diel_sp_no_night_photon_model)
        diel_model_copy = copy.deepcopy(diel_model)

        biomass_adjuster = BiomassAdjuster(diel_model_copy, "BIO_L_Day", "Invalid")

        with self.assertRaises(ValueError):
            biomass_adjuster.total_biomass_reaction()

    def test_total_biomass_reaction_multi_tissue(self):
        diel_sp_no_night_photon_multi_tissue_model = os.path.join(TEST_DIR, "data", "Diel_Multi_Tissue_sp_photon_restricted.xml")
        multi_model = cobra.io.read_sbml_model(diel_sp_no_night_photon_multi_tissue_model)
        multi_model_copy = copy.deepcopy(multi_model)

        biomass_adjuster = BiomassAdjuster(multi_model_copy, "Bio_Nplus_Day", "Bio_Nplus_Night")
        biomass_adjuster.total_biomass_reaction()

        biomass_after = multi_model_copy.reactions.get_by_id("Biomass_Total")
        biomass_before = multi_model.reactions.get_by_id("Bio_Nplus_Night")

        self.assertEqual(2 * (len(biomass_before.reactants)), len(biomass_after.reactants))
        self.assertEqual(2 * (len(biomass_before.products)), len(biomass_after.products))
        self.assertEqual(2 * (len(biomass_before.metabolites)), len(biomass_after.metabolites))

        self.assertIn('Biomass_Total', str(multi_model_copy.objective.expression))

    def test_total_biomass_with_invalid_biomass_reaction_multi_tissue(self):
        diel_sp_no_night_photon_multi_tissue_model = os.path.join(TEST_DIR, "data", "Diel_Multi_Tissue_sp_photon_restricted.xml")
        multi_model = cobra.io.read_sbml_model(diel_sp_no_night_photon_multi_tissue_model)
        multi_model_copy = copy.deepcopy(multi_model)

        biomass_adjuster = BiomassAdjuster(multi_model_copy, "Bio_Nplus_Day", "Invalid")

        with self.assertRaises(ValueError):
            biomass_adjuster.total_biomass_reaction()
