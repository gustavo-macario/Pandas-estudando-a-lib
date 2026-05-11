# 06.01 - Qual a quantidade média de redes sociais dos usuários?
# E a Variância? E o máximo?

# %%
import pandas as pd

df = pd.read_csv('../../clientes.csv', sep=';')  
df['total'] = df['flEmail'] + df['flTwitch'] + df['flYouTube'] + df['flBlueSky'] + df['flInstagram'] + df['flInstagram']

media = df['total'].mean()
variancia = df['total'].var()
maximo = df['total'].max()


print("media:",media)
print("variancia:",variancia)
print("maximo:",maximo)

# %%
