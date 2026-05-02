import pandas as pd

idades = [
    12,
    10,
    20,
    23,
    25,
    30,
    40
]

# tranforma a lista em uma serie
series_idades = pd.Series(idades)
series_idades

# utiliza os metodos de estatisticas da serie
media_idades = series_idades.mean()
var_idades = series_idades.var()
summary_idades = series_idades.describe()
print(summary_idades)
