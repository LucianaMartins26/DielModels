import os
import unittest

import cobra.io
from tests import TEST_DIR


class TestReadModel(unittest.TestCase):

    def test_read_model(self):
        """
        Test reading a model from a file.
        """
        model = cobra.io.read_sbml_model(os.path.join(TEST_DIR, "data", "aragem_photo.xml"))
        self.assertEqual("M_", model.id)

