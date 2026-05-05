# 1- Importe a biblioteca pandas e carregue o arquivo transacoes.csv em um DataFrame chamado df_transacoes, garantindo que as colunas sejam separadas corretamente.
# %% 

import pandas as pd

df_transacoes = pd.read_csv("../data/transacoes.csv", sep=';')


# 2- Filtre o df_transacoes para retornar apenas as linhas onde a coluna QtdePontos seja estritamente maior que 1.
# %%
filtro = df_transacoes["QtdePontos"] > 1
df_transacoes[filtro]



# 3- Retorne um DataFrame contendo apenas os registros onde a coluna DescSistemaOrigem seja exatamente igual a "twitch".
# %%
df_t = df_transacoes["DescSistemaOrigem"]  == 'twitch'
df_transacoes[df_t]



# 4- Crie um filtro composto para retornar as transações onde QtdePontos seja maior ou igual a 10 E menor ou igual a 50.
# %%
filtro_c = (df_transacoes['QtdePontos'] >= 10) & (df_transacoes['QtdePontos'] <= 50)
df_transacoes[filtro_c]



# 5- Filtre o DataFrame para mostrar as linhas onde a DescSistemaOrigem seja "twitch" OU a QtdePontos seja maior que 100.
# %%
filtro2 = (df_transacoes['DescSistemaOrigem'] == "twitch") | (df_transacoes['QtdePontos'] > 100)
df_transacoes[filtro2]



# 6- Utilizando o método .isin(), crie um filtro para retornar os registros cuja DescSistemaOrigem seja "twitch" ou "site".
# %%
filtro3 = df_transacoes['DescSistemaOrigem'].isin(["twitch", "site"])
df_transacoes[filtro3]



# 7- Filtre e retorne todas as linhas onde a coluna IdCliente não seja nula.
# %%
filtro4 = df_transacoes['IdCliente'].notna()
df_transacoes[filtro4]



# 8- Utilizando o operador de negação (~), escreva um código para retornar todas as transações onde a coluna DtCriacao não seja nula.
# %%
filtro5 = ~df_transacoes['DtCriacao'].isna()
df_transacoes[filtro5]



# 9- Filtre os registros onde DescSistemaOrigem é igual a "twitch" e salve o resultado em uma variável chamada df_twitch, garantindo que este novo DataFrame seja uma cópia isolada na memória, desvinculada do original.
# %%
filtro6 = df_transacoes['DescSistemaOrigem'] == "twitch"
df_twitch = df_transacoes[filtro6].copy()
df_twitch



# 10- A partir do df_twitch criado no exercício anterior, crie uma nova coluna chamada "BonusAplicado" e atribua o valor False para todas as linhas desse DataFrame.    
#  %%
df_twitch['BonusAplicado'] = False
df_twitch
