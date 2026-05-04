# %%

import pandas as pd

df_clientes = pd.read_csv("data/clientes.csv")
df_clientes

#---------------------------------------------------------------------------------
# AMOSTRAS
# %%

# '.head()' imprimi as 5 primeiras linhas do df, como se fosse um limit do sql
df_clientes.head()


# %%

# '.tail()' pega os 5 ultimos do df
df_clientes.tail()


# %%

# '.sample(10)' pega valores aleatorios do df
df_clientes.sample(10)

#---------------------------------------------------------------------------------
# %%

# '.shape' retorna o numero de linhas e colunas do df
df_clientes.shape


# %%

# '.columns' exibe o nome de todas as colunas do df
df_clientes.columns


# %%

# '.index' exibe a quantidade de indices do df, o ultimo nao conta, igual o range do python
df_clientes.index


# %%

# '.info()' exibe informacoes com algumas estatisticas sobre o df
df_clientes.info()

# exibe exatamente a quantidade de memoria ram que esta sendo usada no df
df_clientes.info(memory_usage='deep')


#%%

# 'dtypes' retorna uma serie, em que para cada coluna, retorna seu valor, e seus indices sao os proprios nomes das colunas
df_clientes.dtypes