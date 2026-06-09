# %%
import pandas as pd

df = pd.read_csv('base_consolidada.csv', sep=',')
df.head()

# %%
df_stack = (df.set_index(['nome', 'periodo'])
 .stack()
 .reset_index()
 )
df_stack.columns = ['nome', 'periodo', 'metrica', 'valor']
df_stack


# %%
df_stack.pivot(values='valor', 
               index=['nome', 'periodo'], 
               columns='metrica'
               .reset_index())




# %%
# retorna a media da metrica de cada estado em cada tipo de metrica das colunas
df_stack.pivot_table(values='valor', 
               index=['nome'], 
               columns='metrica',
               aggfunc='mean')