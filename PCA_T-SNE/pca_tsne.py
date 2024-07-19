import os.path

import pandas as pd
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
import numpy as np
import re

from tests import TEST_DIR


def pca(df_sampling_path, df_kstest_path):

    df_sampling = pd.read_csv(df_sampling_path)
    df_kstest = pd.read_csv(df_kstest_path)

    differentially_expressed_reactions = df_kstest['Reaction'].tolist()

    columns_to_filter = [column for column in df_sampling.columns if
                         any(reaction in column for reaction in differentially_expressed_reactions)]

    df_filtered = df_sampling[columns_to_filter]

    reactions_data = df_filtered.iloc[:, 1:].values

    pca = PCA(n_components=2)
    pca_result = pca.fit_transform(reactions_data.T)

    variance_ratio = pca.explained_variance_ratio_
    print(sum(variance_ratio))

    pca_df = pd.DataFrame(pca_result, columns=['PC1', 'PC2'])

    labels = ['Day' if 'Day' in reaction else 'Night' for reaction in df_filtered.columns]

    color_map = {'Day': 'orange', 'Night': 'purple'}

    for i, row in pca_df.iterrows():
        category = labels[i]
        color = color_map[category]
        plt.scatter(row['PC1'], row['PC2'], color=color, s=10, marker='o', edgecolors=None)

    for time, color in zip(['Day', 'Night'], ['orange', 'purple']):
        plt.scatter([], [], c=color, s=15, label=time)
    plt.legend(scatterpoints=1, frameon=True, labelspacing=1)

    plt.title('PCA')
    plt.xlabel('Principal Component 1')
    plt.ylabel('Principal Component 2')
    plt.savefig('gráfico_pca_df_filtrado.png')
    plt.show()


def tsne(df_sampling_path, df_kstest_path):

    df_sampling = pd.read_csv(df_sampling_path)
    df_kstest = pd.read_csv(df_kstest_path)

    differentially_expressed_reactions = df_kstest['Reaction'].tolist()

    differentially_expressed_unique_reactions = []

    for reaction in differentially_expressed_reactions:
        if 'reverse' not in reaction:
            differentially_expressed_unique_reactions.append(reaction)

    print('Number of unique differentially expressed reactions:')
    print(len(differentially_expressed_unique_reactions))

    columns_to_filter = [column for column in df_sampling.columns if
                         any(reaction in column for reaction in differentially_expressed_reactions)]

    df_filtered = df_sampling[columns_to_filter]

    reactions_data = df_filtered.iloc[:, 1:].values

    tsne = TSNE(n_components=2)
    tsne_result = tsne.fit_transform(reactions_data.T)

    overlap_threshold = 1

    overlapping_points = []
    overlapping_reactions = []

    for i in range(len(tsne_result)):
        for j in range(i + 1, len(tsne_result)):
            if np.linalg.norm(tsne_result[i] - tsne_result[j]) < overlap_threshold:
                overlapping_points.append((i, j))

    for point in overlapping_points:
        overlapping_reactions.append((df_filtered.columns[point[0]], df_filtered.columns[point[1]]))

    overlapping_reactions_no_reverse = [tuplo for tuplo in overlapping_reactions if ("reverse" not in tuplo[0] and "reverse" not in tuplo[1])]
    overlapping_reactions_day_night = [tuplo for tuplo in overlapping_reactions_no_reverse if ("Day" in tuplo[0] and "Night" in tuplo[1]) or ("Night" in tuplo[0] and "Day" in tuplo[1])]

    print('Number of overlapping day reactions with night reactions (without reverse ones):')
    print(len(overlapping_reactions_day_night))
    print('Overlapping reactions:')
    print(overlapping_reactions_day_night)

    regex = re.compile(r'^([^_]+)')

    def extract(string):
        match = regex.search(string)
        if match:
            return match.group(1)
        else:
            return None

    overlapping_same_reaction_day_night = [
        tuplo for tuplo in overlapping_reactions_day_night
        if extract(tuplo[0]) == extract(tuplo[1])
    ]

    print('Reactions overlapping with themselves (day and night):')
    print(len(overlapping_same_reaction_day_night))
    print('Overlapping reactions:')
    print(overlapping_same_reaction_day_night)

    tsne_df = pd.DataFrame(tsne_result, columns=['t-SNE1', 't-SNE2'])

    labels = ['Day' if 'Day' in reaction else 'Night' for reaction in df_filtered.columns]

    color_map = {'Day': 'orange', 'Night': 'purple'}

    for i, row in tsne_df.iterrows():
        category = labels[i]
        color = color_map[category]
        plt.scatter(row['t-SNE1'], row['t-SNE2'], color=color, s=10, marker='o', edgecolors=None)

    for time, color in zip(['Day', 'Night'], ['orange', 'purple']):
        plt.scatter([], [], c=color, s=15, label=time)
    plt.legend(scatterpoints=1, frameon=True, labelspacing=1)

    plt.title('t-SNE')
    plt.xlabel('Component 1')
    plt.ylabel('Component 2')
    plt.savefig('gráfico_t-sne_df_filtrado.png')
    plt.show()


if __name__ == '__main__':
    df_sampling_path = os.path.join(TEST_DIR, 'reconstruction_results', 'MODEL1507180028','results_troppo', 'DielModel',
                              'dfa', 'diel_model_sampling.csv')

    df_kstest_path = os.path.join(TEST_DIR, 'reconstruction_results', 'MODEL1507180028','results_troppo', 'DielModel',
                              'dfa', 'diel_model_DFA_reaction_result.csv')

    pca(df_sampling_path, df_kstest_path)
    tsne(df_sampling_path, df_kstest_path)
