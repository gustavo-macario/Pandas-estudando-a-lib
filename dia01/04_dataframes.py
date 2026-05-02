import pandas as pd

idades = [
    12, 10, 20, 23, 25, 30, 40
]

nomes = [
    'joao','maria', 'pedro', 'ana', 'gustavo','jose', 'jao'
]

series_idades = pd.Series(idades)
series_nomes = pd.Series(nomes)

# dataframes é como se fosse um varal, na qual voce pode pendurar as suas series e nomear elas
df = pd.DataFrame()
df['idades'] = series_idades
df['nomes'] = series_nomes
# vai exibir todo o 'varal' com as series nele, e seu retorno é um dataframe
print(df)
# vai exibir somente a serie nomes, e seu retorno tambem é uma serie, e os indices serao os mesmos do dataframe
print(df['nomes'])
# para pegar a primeira linha de um df usasse iloc, seu retorno é uma serie
print(df.iloc[0]['nomes'])
# pegando a idade da ultima pessoa
print(df.iloc[-1]['idades'])
