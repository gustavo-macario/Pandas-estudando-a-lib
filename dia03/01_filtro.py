# %%

import pandas as pd

df = pd.read_csv("../data/transacoes.csv", sep=";")
df.head() 


# %%

# filtrando o df, retorna uma serie de booleanos
filtro = df["QtdePontos"] >= 50
df[filtro]



# %%

# filtrando o df com dois filtros
filtro = (df["QtdePontos"] >= 50) & (df["QtdePontos"] < 100)
df[filtro]



# %%

filtro (df["QtdePontos"] == 1) | (df["QtdePontos"] == 100)
df[filtro]