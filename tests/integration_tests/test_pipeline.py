from unittest import TestCase

import cobra
import os

from cobra.flux_analysis import pfba

from tests import TEST_DIR

from diel_models.diel_models_creator import diel_models_creator


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
                                    "S_L_45_Tyrosine_c[C_c]", "S_L_45_Alanine_c[C_c]",
                                    "S_L_45_Asparagine_c[C_c]", "S_L_45_Serine_c[C_c]",
                                    "S_L_45_Aspartate_c[C_c]", "S_Starch_p[C_p]",
                                    "S_D_45_Fructose_c[C_c]", "S__40_S_41__45_Malate_c[C_c]",
                                    "S_Fumarate_c[C_c]", "S_Citrate_c[C_c]"]

        diel_models_creator(modelo, storage_pool_metabolites, ["Ex16"],["Ex4"],"BIO_L")

        for reaction in modelo.reactions:
            if 'Biomass' not in reaction.id:
                assert "_Day" in reaction.id or "_Night" in reaction.id, "The model does not have Day and Night reactions."
        for metabolite in modelo.metabolites:
            assert "_Day" in metabolite.id or "_Night" in metabolite.id or "sp" in metabolite.id, "The model does not " \
                                                                                                  "have Day, Night or " \
                                                                                                  "sp metabolites."
        for compartment in modelo.compartments:
            assert "_Day" in compartment or "_Night" in compartment or 'sp' in compartment, "The model does not have day " \
                                                                                            "or night or " \
                                                                                            "storage pool compartments"
        self.assertEqual(modelo.reactions.get_by_id("Ex16_Night").bounds, (0, 0))
        self.assertEqual(modelo.reactions.get_by_id("BIO_L_Day").bounds, (0, 0))
        self.assertEqual(modelo.reactions.get_by_id("BIO_L_Night").bounds, (0, 0))

        self.assertIn('Biomass_Total', str(modelo.objective.expression))

        nitrate_uptake_reaction_day = modelo.reactions.get_by_id("Ex4_Day")
        nitrate_uptake_reaction_night = modelo.reactions.get_by_id("Ex4_Night")

        solution = pfba(modelo).fluxes

        self.assertEqual(round(solution[nitrate_uptake_reaction_day.id] * 2, 4),
                         round(solution[nitrate_uptake_reaction_night.id] * 3, 4))

    def test_pipeline_multi_tissue(self):
        multi_tissue_model_path = os.path.join(TEST_DIR, 'data', 'TS4_Model_lv3.xml')

        multi_tissue = cobra.io.read_sbml_model(multi_tissue_model_path)

        storage_pool_metabolites = ['C00095[c]', 'C00095[d]', 'C00099[d]',
                                  'C00099[c]', 'C00064[c]', 'C00064[d]',
                                  'C00042[c]', 'C00042[d]', 'C00089[c]',
                                  'C00089[d]', 'C00122[c]', 'C00122[d]']

        diel_models_creator(multi_tissue, storage_pool_metabolites, ["ExMe15", "ExBe15"], ["ExBe10"], "Bio_Nplus",
                            tissues = ["Bundle Sheath", "Mesophyll"])

        for reaction in multi_tissue.reactions:
            if 'Biomass' not in reaction.id:
                assert "_Day" in reaction.id or "_Night" in reaction.id, "The model does not have Day and Night reactions."
        for metabolite in multi_tissue.metabolites:
            assert "_Day" in metabolite.id or "_Night" in metabolite.id or "sp" in metabolite.id, "The model does not " \
                                                                                                  "have Day, Night or " \
                                                                                                  "sp metabolites."
        for compartment in multi_tissue.compartments:
            assert "_Day" in compartment or "_Night" in compartment or 'sp' in compartment, "The model does not have day " \
                                                                                            "or night or " \
                                                                                            "storage pool compartments"
        self.assertEqual(multi_tissue.reactions.get_by_id("ExBe15_Night").bounds, (0, 0))
        self.assertEqual(multi_tissue.reactions.get_by_id("ExMe15_Night").bounds, (0, 0))
        self.assertEqual(multi_tissue.reactions.get_by_id("Bio_Nplus_Day").bounds, (0, 0))
        self.assertEqual(multi_tissue.reactions.get_by_id("Bio_Nplus_Night").bounds, (0, 0))

        self.assertIn('Biomass_Total', str(multi_tissue.objective.expression))

        for nitrate_uptake_reaction_day, nitrate_uptake_reaction_night in zip(["ExBe10_Day"], ["ExBe10_Night"]):
            nitrate_reaction_day = multi_tissue.reactions.get_by_id(nitrate_uptake_reaction_day)
            nitrate_reaction_night = multi_tissue.reactions.get_by_id(nitrate_uptake_reaction_night)

            solution = pfba(multi_tissue).fluxes

            self.assertEqual(round(solution[nitrate_reaction_day.id] * 2, 4),
                             round(solution[nitrate_reaction_night.id] * 3, 4))