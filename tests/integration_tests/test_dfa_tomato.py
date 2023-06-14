import os
from unittest import TestCase

import cobra.io

from DFA.differential_flux_analysis_tomato import DFA, split_reversible_reactions
from tests import TEST_DIR
import pandas as pd


class TestDFATomato(TestCase):

    def setUp(self) -> None:
        self.model_id = 'TOMATOMODEL'
        self.dataset_id = 'TomatoDielModel'
        self.model_specifics = {'tomato_diel_model': 'Tomato_Diel_Model'}
        self.objectives = {'tomato_diel_model': 'Biomass_Total'}
        self.results_folder = os.path.join(TEST_DIR, 'reconstruction_results', self.model_id, 'results_troppo',
                                           self.dataset_id, 'dfa')
        self.dfa = DFA(self.model_id, self.dataset_id, self.model_specifics, self.objectives)
        self.model_to_sample = cobra.io.read_sbml_model(os.path.join(TEST_DIR, 'reconstruction_results',
                                                                     self.model_id, 'results_troppo',
                                                                     self.dataset_id, 'reconstructed_models',
                                                                     'Tomato_Diel_Model.xml'))

    def test_sampling(self) -> None:
        day_sampling, night_sampling = self.dfa.sampling(thinning=100, n_samples=1000)

        result_model = split_reversible_reactions(self.model_to_sample)
        exchanges_demands_sinks = [reaction.id for reaction in self.model_to_sample.exchanges] + \
                                  [reaction.id for reaction in self.model_to_sample.demands] + \
                                  [reaction.id for reaction in self.model_to_sample.sinks]
        exchanges_demands_sinks = set(exchanges_demands_sinks)

        for reaction in result_model.reactions:
            if reaction not in exchanges_demands_sinks and reaction.id.endswith("_reverse") \
                    and reaction.lower_bound < 0 < reaction.upper_bound:
                self.assertTrue(reaction.id.replace("_reverse", "") in self.model_to_sample.reactions)
                original_reaction = self.model_to_sample.reactions.get_by_id(reaction.id.replace("_reverse", ""))
                self.assertEqual(reaction.lower_bound, 0)
                self.assertEqual(reaction.upper_bound, -original_reaction.lower_bound)
                for metabolite, coefficient in reaction.metabolites.items():
                    self.assertEqual(coefficient, -original_reaction.metabolites[metabolite])

        self.assertIsInstance(day_sampling, pd.DataFrame)
        self.assertIsInstance(night_sampling, pd.DataFrame)

        self.assertFalse(day_sampling.empty)
        self.assertFalse(night_sampling.empty)

        self.assertEqual(len(day_sampling), len(night_sampling))

        self.assertTrue(all('Day' in column for column in day_sampling.columns))
        self.assertTrue(all('Night' in column for column in night_sampling.columns))

        for modelname in self.model_specifics:
            expected_file = os.path.join(self.results_folder, '%s_sampling.csv' % modelname)
            self.assertTrue(os.path.exists(expected_file))

    def test_ktest(self) -> None:

        self.dfa.sampling()
        results = self.dfa.kstest()

        self.assertIsInstance(results, list)
        self.assertNotIn("Day", results)
        self.assertNotIn("Night", results)

        for modelname in self.model_specifics:
            expected_file = os.path.join(self.results_folder, '%s_DFA_reaction_result.csv' % modelname)
            self.assertTrue(os.path.exists(expected_file))

        result_df = pd.read_csv(expected_file)

        self.assertIsInstance(result_df, pd.DataFrame)

        expected_columns = ['Reaction', 'Pvalue', 'Padj', 'Reject', 'FC']
        self.assertListEqual(list(result_df.columns), expected_columns)
