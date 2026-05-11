# %%
# 06.02 - Quais são os usuários que mais fizeram transações?
# Considere os 10 primeiros.
import pandas as pd

df = pd.read_csv("../../data/transacoes.csv", sep=';')

(df.groupby(by=['IdCliente'])['IdTransacao'].count()
.sort_values(ascending=False)
.head(10))
