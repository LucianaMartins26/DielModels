import os

import cobra
import pandas as pd

from tests import TEST_DIR

if __name__ == '__main__':
    luciana_diel_model = cobra.io.read_sbml_model("quercus/(changed)diel_multi_quercus_model.xml")
    emanuel_diel_model = cobra.io.read_sbml_model(os.path.join(TEST_DIR, 'models', 'Emanuel_DielMultiTissueModel.xml'))

    data_simulation = {luciana_diel_model.summary(), emanuel_diel_model.summary()}

    tabel1 = pd.DataFrame(data_simulation)

    tabel1.index = ["Original Diel Multi Tissue Quercus", "Created Diel Multi Tissue Quercus"]

    tabel1.to_csv('Quercus_Diel_MultiTissue_Models_Comparison.csv', sep=',')

    print(tabel1)