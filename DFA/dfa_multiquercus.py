import os
import cobra.io

from differential_flux_analysis import DFA
from tests import TEST_DIR


class DFAMultiQuercus:

    def __init__(self) -> None:
        self.model_id = 'MultiTissueQuercusModel'
        self.dataset_id = 'MultiQuercusDielModel'
        self.model_specifics = {'multi_quercus_diel_model': 'Multi_Quercus_Diel_Model'}
        self.objectives = {'multi_quercus_diel_model': 'Total_biomass'}
        self.results_folder = os.path.join(TEST_DIR, 'reconstruction_results', self.model_id, 'results_troppo',
                                           self.dataset_id, 'dfa')
        self.dfa = DFA(self.model_id, self.dataset_id, self.model_specifics, self.objectives)
        self.model_to_sample = cobra.io.read_sbml_model(os.path.join(TEST_DIR, 'reconstruction_results', self.model_id,
                                                                     'results_troppo', self.dataset_id,
                                                                     'reconstructed_models',
                                                                     'Multi_Quercus_Diel_Model.xml'))

    def sampling(self) -> None:
        self.dfa.sampling(thinning=100, n_samples=1000)

    def ktest(self) -> None:
        self.dfa.sampling()
        self.dfa.kstest()


if __name__ == '__main__':
    dfa = DFAMultiQuercus()
    dfa.sampling()
    dfa.ktest()
