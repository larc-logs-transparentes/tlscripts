import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

sns.set_theme(style="whitegrid")

df = pd.read_csv("timeline.csv")
df = df[df['codigo_candidato'] != 'branco']
df = df[df['codigo_candidato'] != 'nulo']

if not os.path.exists("output_graphs"):
    os.mkdir("output_graphs")


for cargo in df['cargo'].unique():
    df_cargo = df.loc[df['cargo'] == cargo]

    for quantidade_bus_somados in df_cargo['quantidade_bus_somados'].unique():
        total_votes = df_cargo.loc[df_cargo['quantidade_bus_somados'] == quantidade_bus_somados, 'quantidade_votos'].sum()
        df_cargo.loc[df_cargo['quantidade_bus_somados'] == quantidade_bus_somados, 'percentage'] = df_cargo.loc[df_cargo['quantidade_bus_somados'] == quantidade_bus_somados, 'quantidade_votos'] / total_votes * 100
        print(df_cargo.loc[df_cargo['quantidade_bus_somados'] == quantidade_bus_somados].head())

    plt.figure()
    sns.lineplot(data=df_cargo, x="quantidade_bus_somados", y="percentage", hue="codigo_candidato")

    plt.title(f"{cargo.capitalize()}")
    plt.xlabel("Resultado parcial")
    plt.ylabel("Porcentagem de votos")

    plt.savefig(f"output_graphs/{cargo}.png")
