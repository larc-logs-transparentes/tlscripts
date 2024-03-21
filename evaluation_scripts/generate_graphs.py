import os

import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
sns.set_theme(style="whitegrid")


def plot_proofs_df(df_inclusion_proof, df_consistency_proof):
    # sns.lineplot(data=df_inclusion_proof, color='gray', alpha=0.1, legend=False)
    # sns.lineplot(data=df_consistency_proof, color='gray', alpha=0.1, legend=False)

    mean_inclusion_proof = df_inclusion_proof.mean(axis=1)
    sns.lineplot(data=mean_inclusion_proof, label='Inclusion proof')
    standard_deviation_inclusion_proof = df_inclusion_proof.std(axis=1)
    plt.fill_between(mean_inclusion_proof.index, mean_inclusion_proof - standard_deviation_inclusion_proof, mean_inclusion_proof + standard_deviation_inclusion_proof, alpha=0.5, label='Standard deviation')

    mean_consistency_proof = df_consistency_proof.mean(axis=1)
    sns.lineplot(data=mean_consistency_proof, label='Consistency proof')
    standard_deviation_consistency_proof = df_consistency_proof.std(axis=1)
    plt.fill_between(mean_consistency_proof.index, mean_consistency_proof - standard_deviation_consistency_proof, mean_consistency_proof + standard_deviation_consistency_proof, alpha=0.5, label='Standard deviation')

    plt.legend()

    plt.ylabel('Seconds')
    plt.xlabel('Tree size')
    plt.title('Proofs verification')
    plt.savefig(f'graphs/proofs_verification_time.png')
    plt.clf()


def plot_df(df, title, ylabel, xlabel, min_value=None, max_value=None, scientific_notation=False):
    # sns.lineplot(data=df, color='gray', alpha=0.1, legend=False)

    mean = df.mean(axis=1)
    sns.lineplot(data=mean, label='Mean')
    standard_deviation = df.std(axis=1)
    plt.fill_between(mean.index, mean - standard_deviation, mean + standard_deviation, alpha=0.5, label='Standard deviation')
    plt.ylim(min_value, max_value)
    if scientific_notation:
        # Permits only 1e-2 scientific notation
        plt.ticklabel_format(style='sci', axis='y', scilimits=(0, 2))

    plt.legend()

    plt.ylabel(ylabel)
    plt.xlabel(xlabel)
    plt.title(title)
    plt.savefig(f'graphs/{title}.png')
    plt.clf()

if __name__ == "__main__":
    # recursive remove
    if os.path.exists('graphs'):
        for root, dirs, files in os.walk('graphs'):
            for file in files:
                os.remove(os.path.join(root, file))
        os.rmdir('graphs')
    os.mkdir('graphs')

    df_data_entry = pd.read_csv('data_entry_verification.csv', index_col=0)
    df_local_tree_consistency = pd.read_csv('local_tree_consistency_verification.csv', index_col=0)
    plot_proofs_df(df_data_entry, df_local_tree_consistency)
    plot_df(df_data_entry, 'Data entry verification', 'Seconds', 'Tree size', 0, 0.0002, True)
    plot_df(df_local_tree_consistency, 'Local tree consistency verification', 'Seconds', 'Tree size', 0, 0.08, True)

    df_sum_bus = pd.read_csv('sum_bus.csv', index_col=0)
    plot_df(df_sum_bus, 'TLSum summation', 'Seconds', 'Pool tapes')

    df_rebuild_tree = pd.read_csv('rebuild_tree.csv', index_col=0)
    plot_df(df_rebuild_tree, 'Rebuild tree', 'Seconds', 'Tree size')

