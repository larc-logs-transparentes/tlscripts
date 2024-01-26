import os

import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
sns.set_theme(style="whitegrid")

def plot_df(df, title, xlabel, ylabel):
    sns.lineplot(data=df, color='gray', alpha=0.2, legend=False)

    mean = df.mean(axis=1)
    sns.lineplot(data=mean, label='Mean')

    std = df.std(axis=1)
    plt.fill_between(mean.index, mean - std, mean + std, alpha=0.5, label='Standard deviation')
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
    plot_df(df_data_entry, 'Data proof', 'Number of data entries', 'Seconds')

    df_sum_bus = pd.read_csv('sum_bus.csv', index_col=0)
    plot_df(df_sum_bus, 'Aggregating votes', 'Number of BUs', 'Seconds')


