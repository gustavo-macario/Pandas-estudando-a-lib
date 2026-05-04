# %%

import pandas as pd

# para importar um arquivo 
df = pd.read_csv("../data/clientes.csv")
df


# %%

# para salvar no diretorio atual como csv
df.to_csv("clientes.csv")
## para salvar no diretorio atual sem os indices
df.to_csv("clientes.csv", index=False)


# %%

# para salvar no diretorio atual como parquet
df.to_parquet("clientes.parquet", index=False)


# %%

# ler o arquivo
df_2 = pd.read_parquet("clientes.parquet")
df_2


# %%

# salvar como excel
df.to_excel("clientes.xlsx", index=False)

df_3 = pd.read_excel("clientes.xlsx")
df_3


# %%

# o sep indica ao Pandas qual caractere divide as colunas no seu arquivo
df_teste = pd.read_csv("../data/teste.csv", sep=";")
df_teste

# %%
