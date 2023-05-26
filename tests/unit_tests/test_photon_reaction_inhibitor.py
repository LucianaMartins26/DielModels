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

        photonrestrictor = PhotonReactionInhibitor(diel_storagepool_model_copy, "Ex16_Night")
        photonrestrictor.restrain()

        photon_night_reaction = diel_storagepool_model_copy.reactions.get_by_id("Ex16_Night")

        self.assertEqual(photon_night_reaction.lower_bound, 0)
        self.assertEqual(photon_night_reaction.upper_bound, 0)

        cobra.io.write_sbml_model(diel_storagepool_model_copy,
                                  os.path.join(TEST_DIR, "data", "Diel_AraGEM_sp_photon_restricted.xml"))

    def test_restrain_with_invalid_reaction(self):
        diel_storagepool_model = os.path.join(TEST_DIR, "data", "Diel_AraGEM_with_storage_pool.xml")
        diel_storagepool_model_2 = cobra.io.read_sbml_model(diel_storagepool_model)
        diel_storagepool_model_copy = copy.deepcopy(diel_storagepool_model_2)

        photonrestrictor = PhotonReactionInhibitor(diel_storagepool_model_copy, "Invalid")

        with self.assertRaises(ValueError):
            photonrestrictor.restrain()
