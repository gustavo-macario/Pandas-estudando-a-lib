# %%

import pandas as pd
import numpy as np

df = pd.read_csv("../data/clientes.csv", sep=';')
df.head() 


# %%

# cria uma nova colun no df e adiciona 100 pontos em todas as linhas da serie. Muito mais perfomatico que usar for ou while
df['pontos_100'] = df['qtdePontos'] + 100



# %%

# soma duas colunas e cria uma nova com base nos resultados
df['emailTwitch'] = df['flEmail'] + df['flTwitch']
df.head()



# %%

# soma todas redes socias para descobrir quantos cada pessoa tem
df["qtdeSocial"] = df["flEmail"] + df["flTwitch"] + df["flYouTube"] + df["flBlueSky"] + df["flInstagram"]
df



# %%

df["todas_social"] = df["flEmail"] * df["flTwitch"] * df["flYouTube"] * df["flBlueSky"] * df["flInstagram"]
df



# %%


df["qtdePontos"].describe()



# %%

# utilizando o numpy para fazer transformacoes de dados. O '+1' serviu para nao dar resultado infinito
df['logPontos'] = np.log(df["qtdePontos"] + 1)


# %%
