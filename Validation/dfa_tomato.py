import os
from unittest import TestCase

import cobra.io

from diel_models.differential_flux_analysis import DFA, split_reversible_reactions
from tests import TEST_DIR
import pandas as pd


class TestDFATomato():

    def setUp(self) -> None:
        self.model_id = 'TOMATOMODEL'
        self.dataset_id = 'TomatoDielModel'
        self.model_specifics = {'tomato_diel_model': 'Tomato_Diel_Model'}
        self.objectives = {'tomato_diel_model': 'Biomass_Total'}
        # self.pathways = os.path.join(TEST_DIR, 'tomato_reconstruction_results', self.model_id,
        #                             'results_troppo', self.dataset_id, 'dfa', 'pathways_map.csv')
        self.results_folder = os.path.join(TEST_DIR, 'reconstruction_results', self.model_id, 'results_troppo',
                                           self.dataset_id, 'dfa')
        self.dfa = DFA(self.model_id, self.dataset_id, self.model_specifics, self.objectives)
        self.model_to_sample = cobra.io.read_sbml_model(os.path.join(TEST_DIR, 'reconstruction_results',
                                                                     self.model_id, 'results_troppo',
                                                                     self.dataset_id, 'reconstructed_models',
                                                                     'Tomato_Diel_Model.xml'))
        print(self.model_to_sample.optimize().objective_value)

    def test_sampling(self) -> None:
        self.dfa.sampling(thinning=100, n_samples=1000)


    def test_ktest(self) -> None:

        self.dfa.sampling()
        results = self.dfa.kstest()

        for modelname in self.model_specifics:
            expected_file = os.path.join(self.results_folder, '%s_DFA_reaction_result.csv' % modelname)

        result_df = pd.read_csv(expected_file)
        expected_columns = ['Reaction', 'Pvalue', 'Padj', 'Reject', 'FC']


if __name__ == '__main__':
    dfa = TestDFATomato()
    dfa.setUp()
    print("Testing sampling")
    dfa.test_sampling()
    dfa.test_ktest()