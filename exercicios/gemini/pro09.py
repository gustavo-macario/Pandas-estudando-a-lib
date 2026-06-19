# %% 
import pandas as pd

# %% 
df_clientes = pd.read_csv('../../data/clientes.csv', sep=';')
df_produtos = pd.read_csv('../../data/produtos.csv', sep=';')
df_transacoes = pd.read_csv('../../data/transacoes.csv', sep=';')
df_transacao_produto = pd.read_csv('../../data/transacao_produto.csv', sep=';')


# %%
# 1 Considerando apenas as transações do ano de 2024, qual mês (1 a 12) registrou a maior quantidade de 
# transações únicas?
df_1 = df_transacoes.copy()
df_1['DtCriacao'] = pd.to_datetime(df_1['DtCriacao'])
df_1 = df_1[df_1['DtCriacao'].dt.year == 2024]
df_1['mes'] = df_1['DtCriacao'].dt.month
df_1 = df_1.groupby('mes')['IdTransacao'].nunique()
df_1 = df_1.sort_values(ascending=False).head(1)
df_1


# %%
# 2  Existem transações (IdTransacao na tabela D) que ocorreram no sistema, mas que por algum erro 
# de banco de dados não possuem nenhum produto vinculado a elas na tabela df_transacao_produto? Se sim, quantas são?
df_2 = df_transacoes.merge(right=df_transacao_produto, how='left', on='IdTransacao')
vazias = df_2['IdProduto'].isnull()
transacoes_vazias = df_2[vazias]
transacoes_vazias.shape[0]


# %%
# 3 O time de vendas quer fazer uma simulação: crie uma função usando .apply() na tabela de produtos que aplique 
# um desconto de 15% apenas nos produtos que custam estritamente mais de R$ 100,00. Os produtos mais baratos 
# mantêm o preço original. Qual seria o novo preço médio de todo o catálogo após essa simulação?
df_3 = df_transacao_produto.copy()
def desconto(p):
    if p > 100:
      return p * 0.85
    else:
        return p
df_3['desconto']= df_3['vlProduto'].apply(desconto)
media = df_3['desconto'].mean()
media
# %%

