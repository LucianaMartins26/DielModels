import os
from unittest import TestCase
from diel_models.differential_flux_analysis import DFA
from project_path import PROJECT_PATH


class TestDFA(TestCase):

    def setUp(self) -> None:
        self.model_id = 'MODEL1507180028'
        self.dataset_id = 'DielModel'
        self.model_specifics = {'diel_model': 'Diel_Model'}
        self.objectives = {'diel_model': 'Biomass_Total'}
        self.pathways = os.path.join(PROJECT_PATH, 'reconstruction_results', self.model_id,
                                     'results_troppo', self.dataset_id, 'dfa', 'pathways_map.csv')

    def test_dfa(self) -> None:
        dfa = DFA(self.model_id, self.dataset_id, self.model_specifics, self.objectives)

        dfa.sampling(thinning=100, n_samples=1000)

    def test_ktest(self) -> None:
        dfa = DFA(self.model_id, self.dataset_id, self.model_specifics, self.objectives)

        dfa.sampling()
        dfa.kstest()

    def test_pathways(self) -> None:
        dfa = DFA(self.model_id, self.dataset_id, self.model_specifics, self.objectives, self.pathways)

        dfa.sampling()
        dfa.kstest()
        dfa.pathway_enrichment()
