# %%
import pandas as pd

df = pd.read_csv('../data/clientes.csv', sep=';')

def get_last_id(x):
    return x.split('-')[-1]

df['idCliente'].apply(get_last_id)
