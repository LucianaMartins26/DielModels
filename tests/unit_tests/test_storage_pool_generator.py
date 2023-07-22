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
                   for reaction_met_id in ["Sucrose_c__Day_sp_exchange", "Sulfate_c__Day_sp_exchange",
                                           "Nitrate_c__Day_sp_exchange", "L-Histidine__Day_sp_exchange",
                                           "Sucrose_c__Night_sp_exchange", "Sulfate_c__Night_sp_exchange",
                                           "Nitrate_c__Night_sp_exchange", "L-Histidine__Night_sp_exchange"])


    def test_create_storage_pool_metabolites_multi_tissue(self):
        multi_tissue_model = os.path.join(TEST_DIR, "data", "Multi_Tissue_day_night.xml")
        multi_model = cobra.io.read_sbml_model(multi_tissue_model)
        multi_model_copy = copy.deepcopy(multi_model)

        storagepool_creator = StoragePoolGenerator(multi_model_copy, ['C00095[c]_Day', 'C00095[d]_Day', 'C00099[d]_Day',
                                                                      'C00099[c]_Day', 'C00064[c]_Day', 'C00064[d]_Day',
                                                                      'C00042[c]_Day', 'C00042[d]_Day', 'C00089[c]_Day',
                                                                      'C00089[d]_Day', 'C00122[c]_Day', 'C00122[d]_Day'],
                                                   ["Bundle Sheath", "Mesophyll"])

        storagepool_creator.create_storage_pool_metabolites()
        self.assertIn("Bundle_Sheath_sp", multi_model_copy.compartments)
        self.assertIn("Mesophyll_sp", multi_model_copy.compartments)

        for metabolite in multi_model_copy.metabolites:
            if metabolite.compartment == "Bundle_Sheath_sp":
                self.assertIn("Bundle_Sheath_sp", metabolite.id)
                self.assertNotIn("Day", metabolite.name)
                self.assertNotIn("Night", metabolite.name)

            if metabolite.compartment == "Mesophyll_sp":
                self.assertIn("Mesophyll_sp", metabolite.id)
                self.assertNotIn("Day", metabolite.name)
                self.assertNotIn("Night", metabolite.name)

    def test_sp_metabolites_with_invalid_metabolite_multi_tissue(self):
        multi_tissue_model = os.path.join(TEST_DIR, "data", "Multi_Tissue_day_night.xml")
        multi_model = cobra.io.read_sbml_model(multi_tissue_model)
        multi_model_copy = copy.deepcopy(multi_model)

        storagepool_creator = StoragePoolGenerator(multi_model_copy, ['C00095[c]_Day', 'C00095[d]_Day', 'C00099[d]_Day',
                                                                      'C00099[c]_Day', 'C00064[c]_Day', 'C00064[d]_Day',
                                                                      'C00042[c]_Day', 'C00042[d]_Day', 'C00089[c]_Day',
                                                                      'C00089[d]_Day', 'C00122[c]_Day', 'C00122[d]_Day',
                                                                      'Invalid'], ["Bundle Sheath", "Mesophyll"])
        with self.assertRaises(ValueError):
            storagepool_creator.create_storage_pool_metabolites()

    def test_sp_metabolites_with_invalid_tissue_multi_tissue(self):
        multi_tissue_model = os.path.join(TEST_DIR, "data", "Multi_Tissue_day_night.xml")
        multi_model = cobra.io.read_sbml_model(multi_tissue_model)
        multi_model_copy = copy.deepcopy(multi_model)

        storagepool_creator = StoragePoolGenerator(multi_model_copy, ['C00095[c]_Day', 'C00095[d]_Day', 'C00099[d]_Day',
                                                                      'C00099[c]_Day', 'C00064[c]_Day', 'C00064[d]_Day',
                                                                      'C00042[c]_Day', 'C00042[d]_Day', 'C00089[c]_Day',
                                                                      'C00089[d]_Day', 'C00122[c]_Day', 'C00122[d]_Day'],
                                                   ["Bundle Sheath", "Xylem"])
        with self.assertRaises(ValueError):
            storagepool_creator.create_storage_pool_metabolites()

    def test_create_storage_pool_reactions_multi_tissue(self):
        multi_tissue_model = os.path.join(TEST_DIR, "data", "Multi_Tissue_day_night.xml")
        multi_model = cobra.io.read_sbml_model(multi_tissue_model)
        multi_model_copy = copy.deepcopy(multi_model)

        storagepool_creator = StoragePoolGenerator(multi_model_copy, ['C00095[c]_Day', 'C00095[d]_Day', 'C00099[d]_Day',
                                                                      'C00099[c]_Day', 'C00064[c]_Day', 'C00064[d]_Day',
                                                                      'C00042[c]_Day', 'C00042[d]_Day', 'C00089[c]_Day',
                                                                      'C00089[d]_Day', 'C00122[c]_Day', 'C00122[d]_Day'],
                                                   ["Bundle Sheath", "Mesophyll"])
        storagepool_creator.create_storage_pool_metabolites()
        storagepool_creator.create_storage_pool_first_reactions()
        storagepool_creator.create_storage_pool_second_reactions()

        self.assertEqual(2 * (len(multi_model_copy.metabolites.query("_sp"))),
                         len(multi_model_copy.reactions.query("_sp_exchange")))

        assert all(reaction_met_id in [reaction.id for reaction in multi_model_copy.reactions.query("_sp_exchange")]
                   for reaction_met_id in ["D-Fructose__Bundle_Sheath_Day_sp_exchange",
                                           "D-Fructose__Mesophyll_Day_sp_exchange",
                                           "B-Alanine__Mesophyll_Day_sp_exchange",
                                           "B-Alanine__Bundle_Sheath_Day_sp_exchange",
                                           "Gln__Bundle_Sheath_Day_sp_exchange",
                                           "Gln__Mesophyll_Day_sp_exchange",
                                           "Suc__Bundle_Sheath_Day_sp_exchange",
                                           "Suc__Mesophyll_Day_sp_exchange",
                                           "Sucrose__Bundle_Sheath_Day_sp_exchange",
                                           "Sucrose__Mesophyll_Day_sp_exchange",
                                           "Fum__Bundle_Sheath_Day_sp_exchange",
                                           "Fum__Mesophyll_Day_sp_exchange",
                                           "D-Fructose__Bundle_Sheath_Night_sp_exchange",
                                           "D-Fructose__Mesophyll_Night_sp_exchange",
                                           "B-Alanine__Mesophyll_Night_sp_exchange",
                                           "B-Alanine__Bundle_Sheath_Night_sp_exchange",
                                           "Gln__Bundle_Sheath_Night_sp_exchange",
                                           "Gln__Mesophyll_Night_sp_exchange",
                                           "Suc__Bundle_Sheath_Night_sp_exchange",
                                           "Suc__Mesophyll_Night_sp_exchange",
                                           "Sucrose__Bundle_Sheath_Night_sp_exchange",
                                           "Sucrose__Mesophyll_Night_sp_exchange",
                                           "Fum__Bundle_Sheath_Night_sp_exchange",
                                           "Fum__Mesophyll_Night_sp_exchange"])