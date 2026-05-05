# %%

import pandas as pd

clientes = pd.read_csv("../data/clientes.csv", sep=";")
clientes


# %%

filtro = clientes["QtdePontos"] == 0
# assim ele so cria uma view, nao faz uma copia do df
# clientes_0 = clientes[filtro]

# para fazer uma copia e separar eles, usasse '.copy()'
clientes_0 = clientes[filtro].copy()

clientes_0["flag_1"] = 1
clientes_0
