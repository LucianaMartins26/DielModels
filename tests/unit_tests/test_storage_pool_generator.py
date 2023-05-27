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

        storagepool_creator = StoragePoolGenerator(diel_model_copy, ["S_Sucrose_c[C_c]_Day", "S_Sulfate_c[C_c]_Day",
                                                                     "S_Nitrate_c[C_c]_Day",
                                                                     "S_L_45_Histidine_c[C_c]_Day",
                                                                     "S_L_45_Isoleucine_c[C_c]_Day",
                                                                     "S_L_45_Leucine_c[C_c]_Day",
                                                                     "S_L_45_Lysine_c[C_c]_Day",
                                                                     "S_L_45_Methionine_c[C_c]_Day",
                                                                     "S_L_45_Phenylalanine_c[C_c]_Day",
                                                                     "S_L_45_Threonine_c[C_c]_Day",
                                                                     "S_L_45_Tryptophan_c[C_c]_Day",
                                                                     "S_L_45_Valine_c[C_c]_Day",
                                                                     "S_L_45_Arginine_c[C_c]_Day",
                                                                     "S_L_45_Cysteine_c[C_c]_Day",
                                                                     "S_L_45_Glutamine_c[C_c]_Day",
                                                                     "S_L_45_Glutamate_c[C_c]_Day",
                                                                     "S_Glycine_c[C_c]_Day",
                                                                     "S_L_45_Proline_c[C_c]_Day",
                                                                     "S_L_45_Tyrosine_c[C_c]_Day",
                                                                     "S_L_45_Alanine_c[C_c]_Day",
                                                                     "S_L_45_Asparagine_c[C_c]_Day",
                                                                     "S_L_45_Serine_c[C_c]_Day",
                                                                     "S_Orthophosphate_c[C_c]_Day",
                                                                     "S_Starch_p[C_p]_Day",
                                                                     "S_D_45_Fructose_c[C_c]_Day",
                                                                     "S__40_S_41__45_Malate_c[C_c]_Day",
                                                                     "S_Fumarate_c[C_c]_Day", "S_Citrate_c[C_c]_Day"])

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

        storagepool_creator = StoragePoolGenerator(diel_model_copy, ["S_Sucrose_c[C_c]_Day", "S_Sulfate_c[C_c]_Day",
                                                                     "S_Nitrate_c[C_c]_Day",
                                                                     "S_L_45_Histidine_c[C_c]_Day",
                                                                     "invalid"])
        with self.assertRaises(ValueError):
            storagepool_creator.create_storage_pool_metabolites()

    def test_create_storage_pool_reactions(self):

        ara_gem_diel_model = os.path.join(TEST_DIR, "data", "AraGEM_day_night.xml")
        diel_model = cobra.io.read_sbml_model(ara_gem_diel_model)
        diel_model_copy = copy.deepcopy(diel_model)

        storagepool_creator = StoragePoolGenerator(diel_model_copy, ["S_Sucrose_c[C_c]_Day", "S_Sulfate_c[C_c]_Day",
                                                                     "S_Nitrate_c[C_c]_Day",
                                                                     "S_L_45_Histidine_c[C_c]_Day"])
        storagepool_creator.create_storage_pool_metabolites()
        storagepool_creator.create_storage_pool_first_reactions()
        storagepool_creator.create_storage_pool_second_reactions()

        self.assertEqual(2 * (len(diel_model_copy.metabolites.query("_sp"))),
                         len(diel_model_copy.reactions.query("_sp_exchange")))

        assert all(reaction_met_id in [reaction.id for reaction in diel_model_copy.reactions.query("_sp_exchange")]
                   for reaction_met_id in ["Sucrose_c_Day_sp_exchange", "Sulfate_c_Day_sp_exchange",
                                           "Nitrate_c_Day_sp_exchange", "L-Histidine_Day_sp_exchange",
                                           "Sucrose_c_Night_sp_exchange", "Sulfate_c_Night_sp_exchange",
                                           "Nitrate_c_Night_sp_exchange", "L-Histidine_Night_sp_exchange"])

        cobra.io.write_sbml_model(diel_model_copy, os.path.join(TEST_DIR, "data", "Diel_AraGEM_with_storage_pool.xml"))
