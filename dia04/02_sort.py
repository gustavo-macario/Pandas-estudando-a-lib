# %%

import pandas as pd

clientes = pd.read_csv("../data/clientes.csv", sep=';')



# %%

# pegar o cliente com mais pontos
max_ponto = clientes["qtdePontos"].max()
filtro = clientes["qtdePontos"] == max_ponto
clientes[filtro]



# %%

# ordena do maior para o menor, pega os 5 primeiros e retorna em um df novo, nao é uma view
clientes.sort_values(by="qtdePontos", ascending=False).head(5)


# mesma coisa do de cima mas retorna apenas os id dos clientes, e no formato de serie
top_5 = (clientes.sort_values(by="qtdePontos", ascending=False)
                 .head(5)["idCliente"] )




# %%

brinquedo = pd.DataFrame(
    {
        "nome": ["teo", "ana", "nah", "jose"],
        "idade": [32, 43, 35, 42],
        "salario":[2345, 4533, 3245, 4533],
    }
)

brinquedo

# %%

# ordena por salario em desc, caso der empate, usasse a idade em ordem descrescente para desempatar
brinquedo.sort_values(by=["salario", "idade"], ascending=False)

# ordena por salario em desc, caso der empate, usasse a idade em ordem crescente para desempatar
brinquedo.sort_values(by=["salario", "idade"], ascending=[False, True])