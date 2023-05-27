import os
from scipy.stats import hypergeom
import statsmodels.api
from cobra.sampling import ACHRSampler
from cobra.io import read_sbml_model
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.stats.multitest
import scipy.stats as sp


def split_reversible_reactions(model_to_sample):
    exchanges_demands_sinks = [reaction.id for reaction in model_to_sample.exchanges] + [reaction.id for reaction in
                                                                                         model_to_sample.demands] + [
                                  reaction.id for reaction in model_to_sample.sinks]
    exchanges_demands_sinks = set(exchanges_demands_sinks)
    new_reactions = []
    for reaction in model_to_sample.reactions:
        if reaction not in exchanges_demands_sinks:
            if reaction.lower_bound < 0 < reaction.upper_bound:
                new_reaction = reaction.copy()
                new_reaction.id = reaction.id + "_reverse"
                new_reaction.lower_bound = 0
                new_reaction.upper_bound = -reaction.lower_bound
                for metabolite, coefficient in new_reaction.metabolites.items():
                    new_reaction.add_metabolites({metabolite: -coefficient})
                    new_reaction.add_metabolites({metabolite: -coefficient})
                new_reactions.append(new_reaction)
                reaction.lower_bound = 0
    model_to_sample.add_reactions(new_reactions)
    return model_to_sample


class DFA:
    """
    Class to perform differential flux analysis between metabolic models based on the paper from
    ...
    """

    def __init__(self, modelid, datasetid, specific_models: dict, models_objective: dict, pathways_map: str = None):
        """
        Parameters
        ----------
        modelid: str
            model used to reconstruct the specific models
        datasetid: str
            datasets used to reconstruct the specific models
        specific_models: dict
            name of the model for each tissue
        models_objective: dict
            objective reactions to maximize in simulations
        pathways_map: str, Optional
            path of the csv file containing the pathway of each reaction
        """

        self.models_folder = os.path.join("C:\\Users\\lucia\\Desktop\\DielModels", 'reconstruction_results', modelid,
                                          'results_troppo', datasetid, 'reconstructed_models')

        self.results_folder = os.path.join("C:\\Users\\lucia\\Desktop\\DielModels", 'reconstruction_results', modelid,
                                           'results_troppo', datasetid, 'dfa')

        self.specific_models = specific_models
        self.objectives = models_objective
        self.sampled_fluxes = None
        self.day_sampling = None
        self.night_sampling = None
        self.pathways = pathways_map
        self.results = None

    def sampling(self, thinning: int = 100, n_jobs: int = 4, n_samples: int = 100):
        """
        Performs flux sampling
        Parameters
        -------
        thinning: int (default = 100)
            the thinning factor of the generated sampling chain. A thinning of
            10 means samples are returned every 10 steps
        n_jobs: int (default = 4)
            number of threads to use for flux sampling (not working??)
        n_samples: int (default = 100)
            number os samples to be returned
        Returns
        -------
        day_sampling: pandas DataFrame
            sampled fluxes for the daytime
        night_sampling: pandas DataFrame
            sampled fluxes for the nighttime
        """

        day_sampling_dic = {}
        night_sampling_dic = {}
        model_sampling_dic = {}

        for modelname in self.specific_models:
            try:
                df_sampling = pd.read_csv(os.path.join(self.results_folder, '%s_sampling.csv' % modelname),
                                          index_col=0)
            except FileNotFoundError:
                model_path = os.path.join(self.models_folder, '%s.xml' % (self.specific_models[modelname]))
                model_obj = read_sbml_model(model_path)

                model_obj = split_reversible_reactions(model_obj)

                model_obj.objective = self.objectives[modelname]

                model_obj.objective_direction = 'max'

                sampling = ACHRSampler(model_obj, thinning=thinning, n_jobs=n_jobs)
                df_sampling = sampling.sample(n_samples)
                df_sampling.to_csv(os.path.join(self.results_folder, '%s_sampling.csv' % modelname))

            df_day = df_sampling[df_sampling.columns[(df_sampling.columns.str.endswith('_Day')) |
                                                     (df_sampling.columns.str.endswith('_Day_reverse'))]]

            df_night = df_sampling[df_sampling.columns[(df_sampling.columns.str.endswith('_Night')) |
                                                       (df_sampling.columns.str.endswith('_Night_reverse'))]]

            day_sampling_dic[modelname] = df_day
            night_sampling_dic[modelname] = df_night
            model_sampling_dic[modelname] = df_sampling

        self.sampled_fluxes = model_sampling_dic

        self.day_sampling = pd.concat(day_sampling_dic.values(), keys=day_sampling_dic.keys())
        self.night_sampling = pd.concat(night_sampling_dic.values(), keys=night_sampling_dic.keys())

        return self.day_sampling, self.night_sampling

    def kstest(self):
        """
        Calculate the K-S test to detect significantly altered reactions fluxes.
        Results are saved in a csv file.

        Returns
        -------
        list: The results of the K-S test for each reaction.

        """

        modelnames = '_'.join(list(self.sampled_fluxes.keys()))

        rxns1 = set(self.day_sampling.columns)
        rxns2 = set(self.night_sampling.columns)
        rxns = rxns1.symmetric_difference(rxns2)  # all reactions

        pvals = []
        rxnid = []
        fc = []

        for rxn in rxns:
            if "_Day" in rxn:
                data1 = self.day_sampling[rxn].round(decimals=4)
                data2 = self.night_sampling[rxn.replace('_Day', '_Night')].round(decimals=4)

                data1 = data1.sample(n=20)
                data2 = data2.sample(n=20)

                if data1.std() != 0 and data1.mean() != 0 and data2.std() != 0 and data2.mean() != 0:
                    kstat, pval = sp.ks_2samp(data1, data2)

                    foldc = (data1.mean() - data2.mean()) / abs(data1.mean() + data2.mean())

                    pvals.append(pval)
                    rxnid.append(rxn.replace("_Day", ""))
                    fc.append(foldc)

        data_mwu = pd.DataFrame({'Reaction': rxnid, 'Pvalue': pvals})
        data_mwu = data_mwu.set_index('Reaction')

        reject, padj, _, _ = statsmodels.stats.multitest.multipletests(data_mwu['Pvalue'], alpha=0.05, method='fdr_bh',
                                                                       is_sorted=False, returnsorted=False)

        data_mwu['Padj'] = padj
        data_mwu['Reject'] = reject
        data_mwu['FC'] = fc

        data_sigFC = data_mwu.loc[(abs(data_mwu['FC']) > 0.82) & (data_mwu['Padj'] < 0.05), :]
        data_sigFC = data_mwu.loc[(data_mwu['Padj'] < 0.05), :]

        file = os.path.join(self.results_folder, '%s_DFA_reaction_result.csv' % modelnames)
        data_sigFC.to_csv(file)

        self.results = data_sigFC.index.to_list()

        return self.results

    def pathway_enrichment(self):
        """
        Maps significantly altered reactions to pathways using the pathways self.pathways.
        Results are saved in csv and jpg files.
        """
        if not self.pathways:
            print('No pathway information is available, not possible to perform pathway enrichment analysis')
            return None

        subs = pd.read_csv(self.pathways, dtype=str)

        dataset = pd.DataFrame()

        for path in subs.columns:
            reaction_set = subs[path]

            rxn = reaction_set.reset_index(drop=True)

            df_temp = pd.DataFrame({path: rxn})

            dataset = pd.concat([dataset, df_temp], axis=1)

        listrxnSize = []
        setSize = []
        results = []

        for reaction in self.results:
            reaction = reaction + "_Day"
            results.append(reaction)

        d = [r for r in results]

        for col in dataset.columns:
            df = pd.DataFrame({'Reaction': dataset[col]})
            df.dropna()

            out = []

            for reac in df['Reaction']:
                if reac in results:
                    out.append(reac)
                    if reac in d:
                        d.remove(reac)

            listrxnSize.append(len(out))
            setSize.append(len(dataset[col].dropna()))

        hyperdata = pd.DataFrame({'Pathways': dataset.columns, 'ListReactions': listrxnSize, 'SetSize': setSize})

        hits = hyperdata['ListReactions']
        pool = hyperdata['SetSize']

        allrxns = hyperdata['SetSize'].sum()
        targetrxns = hyperdata['ListReactions'].sum()

        pvalList = []

        for h, p in zip(hits, pool):
            rv = hypergeom(allrxns - p, p, targetrxns)

            pval = rv.pmf(h)

            pvalList.append(pval)

        hyperdata['P-value'] = pvalList

        reject, padj, _, _ = statsmodels.stats.multitest.multipletests(hyperdata['P-value'], alpha=0.05,
                                                                       method='fdr_bh',
                                                                       is_sorted=False, returnsorted=False)

        hyperdata['P-value_adj'] = padj
        hyperdata['Reject'] = reject

        hyperdata_sig = hyperdata[(hyperdata['Reject']) & (hyperdata['ListReactions'] != 0)]

        hyperdata_sorted = hyperdata_sig.sort_values(by='P-value_adj', ascending=False)
        hyperdata_sorted = hyperdata_sorted[hyperdata_sorted['Pathways'] != 'transporters']
        hyperdata_sorted = hyperdata_sorted[hyperdata_sorted['Pathways'] != 'drains']

        plt.figure(figsize=(12, 10))

        sc = plt.scatter(hyperdata_sorted['P-value_adj'], np.arange(0, len(hyperdata_sorted['Pathways'])),
                         s=hyperdata_sorted['ListReactions'], color=(0.9, 0.3, 0.1, 0.9))

        plt.xlabel('Adjusted p-value')

        plt.yticks(np.arange(0, len(hyperdata_sorted['Pathways'])), labels=hyperdata_sorted['Pathways'])

        try:
            handles, labels = sc.legend_elements(prop="sizes", alpha=0.8)
            plt.legend(handles, labels, bbox_to_anchor=(1.6, 1.02), loc='upper right', title="Reactions")

            plt.tight_layout()

            names = '_'.join(list(self.specific_models.keys()))

            plt.savefig(os.path.join(self.results_folder, '%s_DFA_pathway_result.png' % names), dpi=600)

            hyperdata_sorted.to_csv(os.path.join(self.results_folder, '%s_DFA_pathway_result.csv' % names))
        except ValueError:
            return None

    def run_complete_dfa(self, thinning: int = 100, n_jobs: int = 4):
        """
        Run the three steps of dfa: sampling, ks test and pathway enrichment
        Parameters
        -------
        thinning: int (default = 100)
            the thinning factor of the generated sampling chain. A thinning of
            10 means samples are returned every 10 steps
        n_jobs: int (default = 4)
            number of threads to use for flux sampling (not working??)
        """
        print('Sampling is starting...')
        self.sampling(thinning=thinning, n_jobs=n_jobs)
        print('Sampling is complete!')

        print('Starting KS test')
        self.kstest()
        print('KS is complete!')

        print('Starting Pathway enrichment analysis test')
        self.pathway_enrichment()
        print('Pathway enrichment analysis is complete!')

        print('Differential flux analysis is complete!')


def bootstrapCI(rxn: pd.Series):
    """
    Calculate the confidence interval of a reaction

    Parameters
    ----------
    rxn: pd.Series
        values for the reaction

    Returns
    -------
    int: 1 if the reaction is significantly different from the mean, 0 otherwise.

    """
    bsci = []

    for i in range(1000):
        bt_samp = rxn.sample(1000, replace=True)
        bsci.append(bt_samp.mean())

    ci_low = np.percentile(bsci, 2.5)
    ci_high = np.percentile(bsci, 97.5)

    if ci_low > 0 or ci_high < 0:
        return 1
    else:
        return 0
