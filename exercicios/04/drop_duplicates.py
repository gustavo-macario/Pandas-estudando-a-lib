# Obtenha a última linha de transacao de cada cliente
# Obtenha a primeira

# %%
import pandas as pd

df = pd.read_csv('../../data/transacoes.csv', sep=';')

ultima = (df.sort_values(by='DtCriacao')
          .drop_duplicates(subset=['IdCliente'], keep='last'))

primeira = (df.sort_values(by='DtCriacao')
          .drop_duplicates(subset=['IdCliente'], keep='first'))
# %%
