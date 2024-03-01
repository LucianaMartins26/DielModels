import cobra
import os
from tests import TEST_DIR

if __name__ == '__main__':

    athaliana2013 = cobra.io.read_sbml_model(os.path.join(TEST_DIR, 'models', 'Athaliana_cheung13.xml'))
    diel_athaliana2013 = cobra.io.read_sbml_model(os.path.join(TEST_DIR, 'models', 'diel_thaliana2013_model.xml'))
    
    athaliana2013.objective = "EX_x_Photon"
    athaliana2013.objective_direction = "max"
    diel_athaliana2013.objective = "EX_x_Photon_Day"
    diel_athaliana2013.objective_direction = "max"
    
    maize_C4GEM = cobra.io.read_sbml_model(os.path.join(TEST_DIR, 'models', 'Maize_C4GEM_vs1.0.xml'))
    diel_maize_C4GEM = cobra.io.read_sbml_model(os.path.join(TEST_DIR, 'models', 'diel_maizeC4GEM_model.xml'))

    maize_C4GEM.objective = "EX11"
    maize_C4GEM.objective_direction = "max"
    diel_maize_C4GEM.objective = "EX11_Day"
    diel_maize_C4GEM.objective_direction = "max"
    
    maize_iEB5204 = cobra.io.read_sbml_model(os.path.join(TEST_DIR, 'models', 'Maize_iEB5204.xml'))
    diel_maize_iEB5204 = cobra.io.read_sbml_model(os.path.join(TEST_DIR, 'models', 'diel_maizeiEB5204_model.xml'))
    
    maize_iEB5204.objective = "tx__Light_"
    maize_iEB5204.objective_direction = "max"
    diel_maize_iEB5204.objective = "tx__Light__Day"
    diel_maize_iEB5204.objective_direction = "max"
    
    maize_saha = cobra.io.read_sbml_model(os.path.join(TEST_DIR, 'models', 'Maize_Saha2011_v2.xml'))
    diel_maize_saha = cobra.io.read_sbml_model(os.path.join(TEST_DIR, 'models', 'diel_maize_saha_model.xml'))

    maize_saha.objective = "EX_hv"
    maize_saha.objective_direction = "max"
    diel_maize_saha.objective = "EX_hv_Day"
    diel_maize_saha.objective_direction = "max"

    maize_simons = cobra.io.read_sbml_model(os.path.join(TEST_DIR, 'models', 'Maize_Simons_mat.xml'))
    diel_maize_simons = cobra.io.read_sbml_model(os.path.join(TEST_DIR, 'models', 'diel_maize_simons_model.xml'))

    maize_simons.objective = "ExMe15"
    maize_simons.objective_direction = "max"
    diel_maize_simons.objective = "ExMe15_Day"
    diel_maize_simons.objective_direction = "max"

    multiquercus = cobra.io.read_sbml_model(os.path.join(TEST_DIR, 'models', 'MultiTissueQuercusModel.xml'))
    diel_multiquercus = cobra.io.read_sbml_model(os.path.join(TEST_DIR, 'models', 'diel_multi_quercus_model.xml'))

    multiquercus.objective = "EX_C00205__dra"
    multiquercus.objective_direction = "max"
    diel_multiquercus.objective = "EX_C00205__dra_Day"
    diel_multiquercus.objective_direction = "max"

    quercus = cobra.io.read_sbml_model(os.path.join(TEST_DIR, 'models', 'QuercusSuberGeneralModel.xml'))
    diel_quercus = cobra.io.read_sbml_model(os.path.join(TEST_DIR, 'models', 'diel_quercus_model.xml'))

    quercus.objective = "EX_C00205__dra"
    quercus.objective_direction = "max"
    diel_quercus.objective = "EX_C00205__dra_Day"
    diel_quercus.objective_direction = "max"

    potato = cobra.io.read_sbml_model(os.path.join(TEST_DIR, 'models', 'potato_mat.xml'))
    diel_potato = cobra.io.read_sbml_model(os.path.join(TEST_DIR, 'models', 'diel_potato_model.xml'))

    potato.objective = "RB002"
    potato.objective_direction = "max"
    diel_potato.objective = "RB002_Day"
    diel_potato.objective_direction = "max"

    rice_lakshmanan = cobra.io.read_sbml_model(os.path.join(TEST_DIR, 'models', 'Rice_Lakshmanan_restricted.xml'))
    diel_rice_lakshmanan = cobra.io.read_sbml_model(os.path.join(TEST_DIR, 'models', 'diel_rice_Lakshmanan_restricted.xml'))

    rice_lakshmanan.objective = "EX_photonVis_LPAREN_e_RPAREN_"
    rice_lakshmanan.objective_direction = "max"
    diel_rice_lakshmanan.objective = "EX_photonVis_LPAREN_e_RPAREN__Day"
    diel_rice_lakshmanan.objective_direction = "max"

    rice_OSI1136 = cobra.io.read_sbml_model(os.path.join(TEST_DIR, 'models', 'Rice_OSI1136.sbml'))
    diel_rice_OSI1136 = cobra.io.read_sbml_model(os.path.join(TEST_DIR, 'models', 'diel_rice_OSI1136_model.xml'))

    rice_OSI1136.objective = "chl_Photon_tx"
    rice_OSI1136.objective_direction = "max"
    diel_rice_OSI1136.objective = "chl_Photon_tx_Day"
    diel_rice_OSI1136.objective_direction = "max"

    rice_poolman = cobra.io.read_sbml_model(os.path.join(TEST_DIR, 'models', 'Rice_Poolman.sbml'))
    diel_rice_poolman = cobra.io.read_sbml_model(os.path.join(TEST_DIR, 'models', 'diel_rice_poolman_model.xml'))

    rice_poolman.objective = "chl_Photon_tx"
    rice_poolman.objective_direction = "max"
    diel_rice_poolman.objective = "chl_Photon_tx_Day"
    diel_rice_poolman.objective_direction = "max"

    sorghum = cobra.io.read_sbml_model(os.path.join(TEST_DIR, 'models', 'Sorghum_C4GEM_vs1.0.xml'))
    diel_sorghum = cobra.io.read_sbml_model(os.path.join(TEST_DIR, 'models', 'diel_sorghum_model.xml'))

    sorghum.objective = "EX11"
    sorghum.objective_direction = "max"
    diel_sorghum.objective = "EX11_Day"
    diel_sorghum.objective_direction = "max"

    sugarcane = cobra.io.read_sbml_model(os.path.join(TEST_DIR, 'models', 'SugarCane_C4GEM_vs1.0.xml'))
    diel_sugarcane = cobra.io.read_sbml_model(os.path.join(TEST_DIR, 'models', 'diel_sugarcane_model.xml'))

    sugarcane.objective = "EX11"
    sugarcane.objective_direction = "max"
    diel_sugarcane.objective = "EX11_Day"
    diel_sugarcane.objective_direction = "max"

    colza = cobra.io.read_sbml_model(os.path.join(TEST_DIR, 'models', 'Colza_bna572_plus.xml'))
    diel_colza = cobra.io.read_sbml_model(os.path.join(TEST_DIR, 'models', 'diel_colza_model.xml'))

    colza.objective = "Ex_ph_t"
    colza.objective_direction = "max"
    diel_colza.objective = "Ex_ph_t_Day"
    diel_colza.objective_direction = "max"

    populus = cobra.io.read_sbml_model(os.path.join(TEST_DIR, 'models', 'Populus_iPop7188_fixed.xml'))
    diel_populus = cobra.io.read_sbml_model(os.path.join(TEST_DIR, 'models', 'diel_populus_model_fixed.xml'))

    populus.objective = "EX_light"
    populus.objective_direction = "max"
    diel_populus.objective = "EX_light_Day"
    diel_populus.objective_direction = "max"

    soybean = cobra.io.read_sbml_model(os.path.join(TEST_DIR, 'models', 'Soybean_GSMM.xml'))
    diel_soybean = cobra.io.read_sbml_model(os.path.join(TEST_DIR, 'models', 'diel_soybean_model.xml'))

    soybean.objective = "Photon_tx"
    soybean.objective_direction = "max"
    diel_soybean.objective = "Photon_tx_Day"
    diel_soybean.objective_direction = "max"

    tomato = cobra.io.read_sbml_model(os.path.join(TEST_DIR, 'models', 'tomato_Sl2183.xml'))
    diel_tomato = cobra.io.read_sbml_model(os.path.join(TEST_DIR, 'models', 'diel_tomato2022_model.xml'))

    tomato.objective = "EX_photon_h"
    tomato.objective_direction = "max"
    diel_tomato.objective = "EX_photon_h_Day"
    diel_tomato.objective_direction = "max"

    print(f"Athaliana {athaliana2013.summary()}")
    print(f"Diel Athaliana {diel_athaliana2013.summary()}")
    print(f"Maize C4GEM {maize_C4GEM.summary()}")
    print(f"Diel Maize C4GEM {diel_maize_C4GEM.summary()}")
    print(f"Maize iEB5204 {maize_iEB5204.summary()}")
    print(f"Diel Maize iEB5204 {diel_maize_iEB5204.summary()}")
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
    print(f"Rice OSI1136 {rice_OSI1136.summary()}")
    print(f"Diel Rice OSI1136 {diel_rice_OSI1136.summary()}")
    print(f"Rice Poolman {rice_poolman.summary()}")
    print(f"Diel Rice Poolman {diel_rice_poolman.summary()}")
    print(f"Sorghum {sorghum.summary()}")
    print(f"Diel Sorghum {diel_sorghum.summary()}")
    print(f"Sugarcane {sugarcane.summary()}")
    print(f"Diel Sugarcane {diel_sugarcane.summary()}")
    print(f"Colza {colza.summary()}")
    print(f"Diel Colza {diel_colza.summary()}")
    print(f"Populus {populus.summary()}")
    print(f"Diel Populus {diel_populus.summary()}")
    print(f"Soybean {soybean.summary()}")
    print(f"Diel Soybean {diel_soybean.summary()}")
    print(f"Tomato {tomato.summary()}")
    print(f"Diel Tomato {diel_tomato.summary()}")