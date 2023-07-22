import os
import copy
from unittest import TestCase

import cobra

from diel_models.photon_reaction_inhibitor import PhotonReactionInhibitor
from tests import TEST_DIR


class TestPhotonInhibitor(TestCase):

    def test_restrain(self):
        diel_storagepool_model = os.path.join(TEST_DIR, "data", "Diel_AraGEM_with_storage_pool.xml")
        diel_storagepool_model_2 = cobra.io.read_sbml_model(diel_storagepool_model)
        diel_storagepool_model_copy = copy.deepcopy(diel_storagepool_model_2)

        photonrestrictor = PhotonReactionInhibitor(diel_storagepool_model_copy, ["Ex16_Night"])
        photonrestrictor.restrain()

        photon_night_reaction = diel_storagepool_model_copy.reactions.get_by_id("Ex16_Night")

        self.assertEqual(photon_night_reaction.lower_bound, 0)
        self.assertEqual(photon_night_reaction.upper_bound, 0)

    def test_restrain_with_invalid_reaction(self):
        diel_storagepool_model = os.path.join(TEST_DIR, "data", "Diel_AraGEM_with_storage_pool.xml")
        diel_storagepool_model_2 = cobra.io.read_sbml_model(diel_storagepool_model)
        diel_storagepool_model_copy = copy.deepcopy(diel_storagepool_model_2)

        photonrestrictor = PhotonReactionInhibitor(diel_storagepool_model_copy, ["Invalid"])

        with self.assertRaises(ValueError):
            photonrestrictor.restrain()

    def test_restrain_with_multi_tissue_reactions(self):
        diel_multi_tissue_with_sp = os.path.join(TEST_DIR, "data", "Diel_Multi_Tissue_with_(random)sp.xml")
        multi_model = cobra.io.read_sbml_model(diel_multi_tissue_with_sp)
        multi_model_copy = copy.deepcopy(multi_model)

        photonrestrictor = PhotonReactionInhibitor(multi_model_copy, ["ExMe15_Night", "ExBe15_Night"])
        photonrestrictor.restrain()

        for photon_night_reaction in ["ExMe15_Night", "ExBe15_Night"]:
            photon_reaction = multi_model_copy.reactions.get_by_id(photon_night_reaction)
            self.assertEqual(photon_reaction.lower_bound, 0)
            self.assertEqual(photon_reaction.upper_bound, 0)


    def test_restrain_with_invalid_reaction_multi_tissue(self):
        diel_multi_tissue_with_sp = os.path.join(TEST_DIR, "data", "Diel_Multi_Tissue_with_(random)sp.xml")
        multi_model = cobra.io.read_sbml_model(diel_multi_tissue_with_sp)
        multi_model_copy = copy.deepcopy(multi_model)

        photonrestrictor = PhotonReactionInhibitor(multi_model_copy, ["ExMe15_Night", "Invalid"])

        with self.assertRaises(ValueError):
            photonrestrictor.restrain()
