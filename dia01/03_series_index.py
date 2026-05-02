import pandas as pd

idades = [
    12, 10, 20, 23, 25, 30, 40
]

indexs = [
    'joao','maria', 'pedro', 'ana', 'gustavo','jose', 'jao'
]

series_idades = pd.Series(idades)
# --------------------------------------------------------------------------
# os indices da series funcionam da mesma maneira das keys de um dicionario, entao nao da para pegar o ultimo elemento com [-1] por exemplo.
print(series_idades[6])

# --------------------------------------------------------------------------
# o sort vai ordenar os valores porem para pegar o primeiro valor nao vai ser o indice [0], porque os valores continuam com o mesmo indice da lista original
series_idades_sort = series_idades.sort_values()
print(series_idades_sort)

# --------------------------------------------------------------------------
# para pegar o primeiro elemento ou ultimo independente do indice, utilizasse iloc
print(series_idades_sort.iloc[0])
print(series_idades.iloc[-1])

# --------------------------------------------------------------------------
# com isso, agora podemos usar por exemplo slice e pegar os 3 primeiros elementos igual uma lista
print(series_idades_sort.iloc[:3])
# do ultimo ao primeiro
print(series_idades_sort.iloc[::-1])

# --------------------------------------------------------------------------
# usando o index, é atribuido os nomes as idades como se fossem chaves, assim na busca da serie, retornariam todos os valores mesmo se tiver chaves repetidas, nesse caso caso quisesse pegar o primeiro por exemplo, ai usaria o iloc
series_idades_index = pd.Series(idades, index=indexs)
print(series_idades_index)
#com '[[]]', ele retorna o ultimo elemento, e tambem a chave
print(series_idades_index.iloc[[-1]])

# OBS: .iloc olha a ordem (posição 0, 1, 2...), enquanto a Series direta olha o nome (o rótulo/índice que você deu).
# .iloc: É como o número da cadeira em um cinema (não importa quem sentar lá, a cadeira 1 é sempre a primeira).
# series[]: É como o nome na lista de chamada (você precisa gritar o nome exato da pessoa para ela responder).