# %%
# 05.05 - Selecione a primeira transação diária de cada cliente.
import pandas as pd

transacoes = pd.read_csv("../../data/transacoes.csv")
transacoes.head()

transacoes["data"] = pd.to_datetime(transacoes["dtCriacao"]).dt.date
transacoes = transacoes.sort_values("dtCriacao")
