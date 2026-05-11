# %%
# 06.03 - Qual usuário teve maior quantidade de pontos debitados?
import pandas as pd

transacoes = pd.read_csv("../../data/transacoes.csv", sep=';')
transacoes.head()

filtro = transacoes['QtdePontos'] < 0

(transacoes[filtro].groupby('IdCliente')['QtdePontos']
.sum()
.sort_values(ascending=True)
.head(1))
# %%
