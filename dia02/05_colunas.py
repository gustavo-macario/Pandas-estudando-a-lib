# %%

import pandas as pd

df = pd.read_csv("../data/transacoes.csv", sep=";")
df

# %%

df.shape


# %%

df.info(memory_usage='deep')


# %%

df.dtypes


# %%

# para mudar um nome de uma coluna, 1 argumento passa o nome antigo, 2 argumento o novo nome
enamed_columns = {
   "QtdePontos": "QtPontos",
   "DescSistemaOrigem": "SistemaOrigem"
}

df = df.rename(columns = renamed_columns)

# se usar com 'inplace=True', nao precisa reatribuir o df
# df = df.rename(columns = renamed_columns, inplace=True)

# %%

# para acessar dois valores do df
df[['IdCliente', 'QtPontos']]         



# %%
# SELECT * FROM df
df

# %%
# SELECT idCliente FROM df

df[["IdCliente"]]

# %%

# SELECT idCliente, qtPontos FROM df LIMIT 5
df[["IdCliente", "QtPontos"]].tail(5)

# %%

# SELECT idCliente, idTransacao, qtPontos
# FROM df
# LIMIT 5

df[["IdCliente", "IdTransacao", "QtPontos"]].head(5)

# %%

# para mostrar de forma ordenada
colunas = list(df.columns)
colunas.sort()
colunas

df = df[colunas]
df