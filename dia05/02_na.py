# %% 

import pandas as pd

clientes = pd.read_csv("../data/clientes.csv")
clientes


# %%

# uma maneira de lidar com NaN é simplesmente nao buscar as linhas que tem qualquer valor NaN
clientes.dropna()



# %%

# com 'how='all'', toda a linha tem quer ser NaN para nao retornar ela 
clientes.dropna(how='all')

# com 'how='any'', se tiver ao menos um NaN, ele ja nao traz a linha 
clientes.dropna(how='any')



# %%
df = pd.DataFrame(
    {
        "nome": ["Téo", None, "Nah", "Marcio"],
        "idade": [None, None, 43, 52],
        "salario": [3453,4324,None,5423]
    }
)

# para filtrar por colunas usasse o subset
df.dropna(how='all', subset={'idade', 'salario'})



# %%

# usasse o 'fillna' para preencher os valores NaN
df["idade"] = df["idade"].fillna(0)
df



# %%

# O código identifica valores NaN e os substitui pela média dos valores existentes naquela coluna para não deixar "buracos" nos dados
medias = df[['idade', 'salario']].mean()
df.fillna(medias)

# %%

df["idade"].fillna(df["idade"].mean()).mean()
