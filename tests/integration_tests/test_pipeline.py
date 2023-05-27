from unittest import TestCase

from diel_models.pipeline import Pipeline
import cobra
import os
from tests import TEST_DIR
from diel_models.day_night_creator import DayNightCreator
from diel_models.storage_pool_generator import StoragePoolGenerator
from diel_models.photon_reaction_inhibitor import PhotonReactionInhibitor
from diel_models.biomass_adjuster import BiomassAdjuster
from diel_models.nitrate_uptake_ratio import NitrateUptakeRatioCalibrator


def diel_models_creator(model, storage_pool_metabolites, photon_reaction_id, biomass_reaction_id,
                        nitrate_exchange_reaction):

    storage_pool_metabolites_with_day = [metabolite + "_Day" for metabolite in storage_pool_metabolites]
    photon_reaction_id_night = photon_reaction_id + "_Night"
    biomass_day_id = biomass_reaction_id + "_Day"
    biomass_night_id = biomass_reaction_id + "_Night"
    nitrate_exchange_reaction_night = nitrate_exchange_reaction + "_Night"
    nitrate_exchange_reaction_day = nitrate_exchange_reaction + "_Day"

    steps = [
        DayNightCreator(model),
        StoragePoolGenerator(model, storage_pool_metabolites_with_day),
        PhotonReactionInhibitor(model, photon_reaction_id_night),
        BiomassAdjuster(model, biomass_day_id, biomass_night_id),
        NitrateUptakeRatioCalibrator(model, nitrate_exchange_reaction_day, nitrate_exchange_reaction_night)
    ]

    pipeline = Pipeline(model, steps)
    pipeline.run()
    return pipeline.model


class TestPipelineEndToEnd(TestCase):

    def test_pipeline(self):
        aragem_model_path = os.path.join(TEST_DIR, 'data', 'aragem_photo.xml')

        modelo = cobra.io.read_sbml_model(aragem_model_path)

        storage_pool_metabolites = ["S_Sucrose_c[C_c]", "S_Sulfate_c[C_c]", "S_Nitrate_c[C_c]",
                                    "S_L_45_Histidine_c[C_c]", "S_L_45_Isoleucine_c[C_c]",
                                    "S_L_45_Leucine_c[C_c]", "S_L_45_Lysine_c[C_c]",
                                    "S_L_45_Methionine_c[C_c]", "S_L_45_Phenylalanine_c[C_c]",
                                    "S_L_45_Threonine_c[C_c]", "S_L_45_Tryptophan_c[C_c]",
                                    "S_L_45_Valine_c[C_c]", "S_L_45_Arginine_c[C_c]",
                                    "S_L_45_Cysteine_c[C_c]", "S_L_45_Glutamine_c[C_c]",
                                    "S_L_45_Glutamate_c[C_c]", "S_Glycine_c[C_c]",
                                    "S_L_45_Proline_c[C_c]", "S_L_45_Tyrosine_c[C_c]",
                                    "S_L_45_Alanine_c[C_c]", "S_L_45_Asparagine_c[C_c]",
                                    "S_L_45_Serine_c[C_c]", "S_Orthophosphate_c[C_c]",
                                    "S_Starch_p[C_p]", "S_D_45_Fructose_c[C_c]",
                                    "S__40_S_41__45_Malate_c[C_c]", "S_Fumarate_c[C_c]",
                                    "S_Citrate_c[C_c]"]

        model = diel_models_creator(modelo, storage_pool_metabolites, "Ex16", "BIO_L", "Ex4")

        cobra.io.write_sbml_model(model, "Diel_Model_after_pipeline.xml")
