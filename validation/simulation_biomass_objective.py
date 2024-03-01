import cobra
import os
from tests import TEST_DIR

if __name__ == '__main__':

    maize_saha = cobra.io.read_sbml_model(os.path.join(TEST_DIR, 'models', 'Maize_Saha2011_v2.xml'))
    diel_maize_saha = cobra.io.read_sbml_model(os.path.join(TEST_DIR, 'models', 'diel_maize_saha_model.xml'))

    maize_saha.objective = "Biomass_synthesis"
    maize_saha.objective_direction = "max"
    diel_maize_saha.objective = "Biomass_Total"
    diel_maize_saha.objective_direction = "max"

    maize_simons = cobra.io.read_sbml_model(os.path.join(TEST_DIR, 'models', 'Maize_Simons_mat.xml'))
    diel_maize_simons = cobra.io.read_sbml_model(os.path.join(TEST_DIR, 'models', 'diel_maize_simons_model.xml'))

    maize_saha.objective = "Bio_Nplus"
    maize_saha.objective_direction = "max"
    diel_maize_saha.objective = "Biomass_Total"
    diel_maize_saha.objective_direction = "max"

    multiquercus = cobra.io.read_sbml_model(os.path.join(TEST_DIR, 'models', 'MultiTissueQuercusModel.xml'))
    diel_multiquercus = cobra.io.read_sbml_model(os.path.join(TEST_DIR, 'models', 'diel_multi_quercus_model.xml'))

    multiquercus.objective = "Total_biomass"
    multiquercus.objective_direction = "max"
    diel_multiquercus.objective = "Biomass_Total"
    diel_multiquercus.objective_direction = "max"

    quercus = cobra.io.read_sbml_model(os.path.join(TEST_DIR, 'models', 'QuercusSuberGeneralModel.xml'))
    diel_quercus = cobra.io.read_sbml_model(os.path.join(TEST_DIR, 'models', 'diel_quercus_model.xml'))

    quercus.objective = "e_Biomass_Leaf__cyto"
    quercus.objective_direction = "max"
    diel_quercus.objective = "Biomass_Total"
    diel_quercus.objective_direction = "max"

    potato = cobra.io.read_sbml_model(os.path.join(TEST_DIR, 'models', 'potato_mat.xml'))
    diel_potato = cobra.io.read_sbml_model(os.path.join(TEST_DIR, 'models', 'diel_potato_model.xml'))

    potato.objective = "RBS01"
    potato.objective_direction = "max"
    diel_potato.objective = "Biomass_Total"
    diel_potato.objective_direction = "max"

    rice_lakshmanan = cobra.io.read_sbml_model(os.path.join(TEST_DIR, 'models', 'Rice_Lakshmanan.xml'))
    diel_rice_lakshmanan = cobra.io.read_sbml_model(os.path.join(TEST_DIR, 'models', 'diel_rice_Lakshmanan_model.xml'))

    rice_lakshmanan.objective = "Straw_Biomass"
    rice_lakshmanan.objective_direction = "max"
    diel_rice_lakshmanan.objective = "Biomass_Total"
    diel_rice_lakshmanan.objective_direction = "max"

    colza = cobra.io.read_sbml_model(os.path.join(TEST_DIR, 'models', 'Colza_bna572_plus.xml'))
    diel_colza = cobra.io.read_sbml_model(os.path.join(TEST_DIR, 'models', 'diel_colza_model.xml'))

    colza.objective = "Biomasssynth_u"
    colza.objective_direction = "max"
    diel_colza.objective = "Biomass_Total"
    diel_colza.objective_direction = "max"

    populus = cobra.io.read_sbml_model(os.path.join(TEST_DIR, 'models', 'Populus_iPop7188.xml'))
    diel_populus = cobra.io.read_sbml_model(os.path.join(TEST_DIR, 'models', 'diel_populus_model.xml'))

    populus.objective = "BiomassRxn"
    populus.objective_direction = "max"
    diel_populus.objective = "Biomass_Total"
    diel_populus.objective_direction = "max"

    tomato = cobra.io.read_sbml_model(os.path.join(TEST_DIR, 'models', 'tomato_Sl2183.xml'))
    diel_tomato = cobra.io.read_sbml_model(os.path.join(TEST_DIR, 'models', 'diel_tomato2022_model.xml'))

    tomato.objective = "BIOMASS_STEM"
    tomato.objective_direction = "max"
    diel_tomato.objective = "Biomass_Total"
    diel_tomato.objective_direction = "max"

    print(f"Maize Saha {maize_saha.summary()}")
    print(f"Diel Maize Saha {diel_maize_saha.summary()}")
    print(f"Maize Simons {maize_simons.summary()}")
    print(f"Diel Maize Simons {diel_maize_simons.summary()}")
    print(f"Multi Quercus {multiquercus.summary()}")
    print(f"Diel Multi Quercus {diel_multiquercus.summary()}")
    print(f"Quercus {quercus.summary()}")
    print(f"Diel Quercus {diel_quercus.summary()}")
    print(f"Potato {potato.summary()}")
    print(f"Diel Potato {diel_potato.summary()}")
    print(f"Rice Lakshmanan {rice_lakshmanan.summary()}")
    print(f"Diel Rice Lakshmanan {diel_rice_lakshmanan.summary()}")
    print(f"Colza {colza.summary()}")
    print(f"Diel Colza {diel_colza.summary()}")
    print(f"Populus {populus.summary()}")
    print(f"Diel Populus {diel_populus.summary()}")
    print(f"Tomato {tomato.summary()}")
    print(f"Diel Tomato {diel_tomato.summary()}")