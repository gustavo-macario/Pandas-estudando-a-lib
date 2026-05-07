# %%

import pandas as pd


# %%

df = pd.read_csv("../data/clientes.csv")

# para converter como outro tipo usasse o 'astype', o retorno é em serie
df['qtdePontos'].astype(float)



# %%

# usasse o replace para trocar um valor por outro ja definido, nessa caso usamos para corrigir onde estava com valor de data zerado resultando em erros
replace = {"0000-00-00 00:00:00.000": "2024-02-01 09:00:00.000"}

# depois de corrijir o erro de data, usamos o 'to_datetime' para converter para data
df["dtCriacao"] = pd.to_datetime(df["dtCriacao"].replace(replace))



# para pegar apenas o mes
df["dtCriacao"].dt.month