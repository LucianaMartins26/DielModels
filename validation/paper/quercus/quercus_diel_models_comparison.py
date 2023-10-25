import cobra
import os
from tests import TEST_DIR

if __name__ == '__main__':
    luciana_diel_model = cobra.io.read_sbml_model(os.path.join(TEST_DIR, 'models', "diel_quercus_model.xml"))
    emanuel_diel_model = cobra.io.read_sbml_model(os.path.join(TEST_DIR, 'models', 'emanuel_diel_model_leaf.xml'))

    luciana_diel_model.objective = 'Biomass_Total'
    luciana_diel_model.objective_direction = 'max'

    emanuel_diel_model.objective = 'e_Biomass_Leaf__cyto_Light'
    emanuel_diel_model.objective_direction = 'max'

    print(f'diel_model: {luciana_diel_model.summary()}')
    print(f'diel_model_leaf: {emanuel_diel_model.summary()}')
