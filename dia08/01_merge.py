# %% 
import pandas as pd

transacoes= pd.read_csv('../data/transacoes.csv', sep=';')
transacoes.head()

# %%
clientes= pd.read_csv('../data/clientes.csv', sep=';')
clientes.head()



# %%
# para dar join usasse o merge, o suffixes é como se fosse um 'as' do sql
transacoes.merge(right=clientes, how='left', on=['IdCliente'], suffixes=['Transacao', 'Clientes'])




# %%
df_1 = pd.DataFrame({
    "transacao": [1,2,3,4,5],
    "nome": ["t1", "t2", "t3", "t4", "t5"],
    "idCliente": [1,2,3,2,2],
    "valor": [10,45,32,17,87],
})

df_2 = pd.DataFrame({
    "id": [1,2,3,4],
    "nome": ["teo", "nah", "mah", "jose"],
})

# exemplo de como dar join quando as colunas nao tem exatamente o mesmo nome
df_1.merge(
    df_2,
    left_on=["idCliente"],
    right_on=["id"],
    how='left',
    suffixes=["Transacao", "Cliente"],
)