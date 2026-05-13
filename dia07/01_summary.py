# %%
import pandas as pd

idades = [32,44,12,54,67,32,23,34,32,12,45,43,28,73,29]
idades = pd.Series(idades)
idades.sum()
idades.min()
idades.max()
idades.mean()
idades.describe()

# %%
clientes = pd.read_csv("../data/clientes.csv", sep=';')
clientes


# %%
clientes['flTwitch'].sum()
clientes['flTwitch'].mean()


# %%
redes_sociais = ["flEmail","flTwitch","flYouTube","flBlueSky","flInstagram"]
clientes[redes_sociais].sum()



# %%
#pegar todas as colunas numericas
num_colums = clientes.dtypes[~clientes.dtypes == 'object'].index.tolist()

clientes[num_colums].mean()



# %%
# com describe ele retorna todas as informacoes estatisticas de todas as colunas
clientes[num_colums].describe()
