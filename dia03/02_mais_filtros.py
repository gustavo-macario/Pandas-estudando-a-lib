# %%

import pandas as pd

df = pd.read_csv("../data/transacao_produto.csv", sep=";")
df


# %%
filtro = (df["IdProduto"] == 5) | (df["IdProduto"] == 11)
df[filtro]



# %%

# outra opcao de filtro com isin
filtro = df["IdProduto"].isin([5,11])
filtro


# %%

clientes = pd.read_csv("../data/clientes.csv", sep=";")

# filtrar valores que nao sao nulos
filtro = clientes["DtCriacao"].notna()
clientes[filtro]


# ~ serve para negacao, mesma coisa do '!'
~clientes["DtCriacao"].isna()

