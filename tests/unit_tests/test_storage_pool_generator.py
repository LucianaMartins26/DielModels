import os
import copy
from unittest import TestCase

import cobra

from diel_models.storage_pool_generator import StoragePoolGenerator
from tests import TEST_DIR


class TestStoragePool(TestCase):

    def test_create_storage_pool_metabolites(self):
        ara_gem_diel_model = os.path.join(TEST_DIR, "data", "AraGEM_day_night.xml")
        diel_model = cobra.io.read_sbml_model(ara_gem_diel_model)
        diel_model_copy = copy.deepcopy(diel_model)

        storagepool_creator = StoragePoolGenerator(diel_model_copy, ["S_Holo_45__91_carboxylase_93__c_Day",
                                                                     "S_Homoeriodictyol_32_chalcone_c_Night",
                                                                     "S_Homogentisate_c_Day", "S_Hordenine_c_Day"])

        storagepool_creator.create_storage_pool_metabolites()
        self.assertIn("sp", diel_model_copy.compartments)

        for metabolite in diel_model_copy.metabolites:
            if metabolite.compartment == "sp":
                self.assertIn("_sp", metabolite.id)
                self.assertNotIn("Day", metabolite.name)
                self.assertNotIn("Night", metabolite.name)

    def test_sp_metabolites_with_invalid_metabolite(self):

        ara_gem_diel_model = os.path.join(TEST_DIR, "data", "AraGEM_day_night.xml")
        diel_model = cobra.io.read_sbml_model(ara_gem_diel_model)
        diel_model_copy = copy.deepcopy(diel_model)

        storagepool_creator = StoragePoolGenerator(diel_model_copy, ["S_Holo_45__91_carboxylase_93__c_Day",
                                                                     "S_Homoeriodictyol_32_chalcone_c_Night",
                                                                     "S_Homogentisate_c_Day", "S_Hordenine_c_Day",
                                                                     "invalid"])
        with self.assertRaises(ValueError):
            storagepool_creator.create_storage_pool_metabolites()

    def test_create_storage_pool_reactions(self):

        ara_gem_diel_model = os.path.join(TEST_DIR, "data", "AraGEM_day_night.xml")
        diel_model = cobra.io.read_sbml_model(ara_gem_diel_model)
        diel_model_copy = copy.deepcopy(diel_model)

        storagepool_creator = StoragePoolGenerator(diel_model_copy, ["S_Holo_45__91_carboxylase_93__c_Day",
                                                                     "S_Homoeriodictyol_32_chalcone_c_Night",
                                                                     "S_Homogentisate_c_Day", "S_Hordenine_c_Day"])
        storagepool_creator.create_storage_pool_metabolites()
        storagepool_creator.create_storage_pool_first_reactions()
        storagepool_creator.create_storage_pool_second_reactions()

        self.assertEqual(2 * (len(diel_model_copy.metabolites.query("_sp"))),
                         len(diel_model_copy.reactions.query("exchange")))

        assert all(reaction_met_id in [reaction.id for reaction in diel_model_copy.reactions.query("exchange")]
                   for reaction_met_id in ["Holo-[carboxylase]_Day_exchange",
                                           "Homoeriodictyolchalcone_Night_exchange",
                                           "Homogentisate_Day_exchange", "Hordenine_Day_exchange",
                                           "Holo-[carboxylase]_Night_exchange",
                                           "Homoeriodictyolchalcone_Day_exchange",
                                           "Homogentisate_Night_exchange", "Hordenine_Night_exchange"])
