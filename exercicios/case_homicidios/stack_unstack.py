# %%
import pandas as pd

df = pd.read_csv('base_consolidada.csv', sep=',')
df.head()



# %%
# transformando as colunas em linhs
df_stack = (df.set_index(["nome", "período"])
      .stack())


# %%
# para definir em df e dar nome as colunas
df_stack = df_stack.reset_index()
df_stack.columns = ["nome", "período", "metrica", "valor"]
df_stack



# %%
# para desempilhar a tabela
df_unstack = (df_stack.set_index(["nome", "período", "metrica"])
                   .unstack()
                   .reset_index()
                   )



# %%
# concertar indice duplicado
metricas = df_unstack.columns.droplevel(0)[2:].tolist()
df_unstack.columns = ['nome', 'período'] + metricas
df_unstack