from unittest import TestCase
from diel_models.differential_flux_analysis import DFA


class TestDFA(TestCase):

    def setUp(self) -> None:
        self.model_id = 'MODEL1507180028'
        self.dataset_id = 'DielModel'
        self.model_specifics = {'diel_model': 'Diel_Model_after_complete_pipeline'}
        self.objectives = {'diel_model': 'Biomass_Total'}

    def test_dfa(self):

        dfa = DFA(self.model_id, self.dataset_id, self.model_specifics, self.objectives)

        dfa.sampling(thinning=100, n_samples=1000)

    def test_ktest(self):
        dfa = DFA(self.model_id, self.dataset_id, self.model_specifics, self.objectives)

        dfa.sampling()
        dfa.kstest()
