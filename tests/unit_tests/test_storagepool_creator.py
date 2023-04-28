import os
import copy
from unittest import TestCase

import cobra

from diel_models.storagepool_creator import StoragePoolCreator
from tests import TEST_DIR


class TestStoragePool(TestCase):

    def test_sp_metabolites(self):
        ara_gem_diel_model = os.path.join(TEST_DIR, "data", "AraGEM_day_night.xml")
        diel_model = cobra.io.read_sbml_model(ara_gem_diel_model)
        diel_model_copy = copy.deepcopy(diel_model)

        storagepool_creator = StoragePoolCreator(diel_model_copy, ["S_Holo_45__91_carboxylase_93__c_Day",
                                                                   "S_Homoeriodictyol_32_chalcone_c_Night",
                                                                   "S_Homogentisate_c_Day", "S_Hordenine_c_Day"])

        storagepool_creator.sp_metabolites()
        self.assertIn("sp", diel_model_copy.compartments)

        for metabolite in diel_model_copy.metabolites:
            if metabolite.compartment == "sp":
                self.assertIn("_sp", metabolite.id)
                self.assertNotIn("Day", metabolite.name)
                self.assertNotIn("Night", metabolite.name)

    def test_sp_reactions(self):

        ara_gem_diel_model = os.path.join(TEST_DIR, "data", "AraGEM_day_night.xml")
        diel_model = cobra.io.read_sbml_model(ara_gem_diel_model)
        diel_model_copy = copy.deepcopy(diel_model)

        storagepool_creator = StoragePoolCreator(diel_model_copy, ["S_Holo_45__91_carboxylase_93__c_Day",
                                                                   "S_Homoeriodictyol_32_chalcone_c_Night",
                                                                   "S_Homogentisate_c_Day", "S_Hordenine_c_Day"])
        storagepool_creator.sp_metabolites()
        storagepool_creator.sp_first_reactions()
        storagepool_creator.sp_second_reactions()

        self.assertEqual(2*(len(diel_model_copy.metabolites.query("_sp"))), len(diel_model_copy.reactions.query("exchange")))
