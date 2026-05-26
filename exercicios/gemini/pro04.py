# %% 
import pandas as pd

# %% 
df_clientes = pd.read_csv('../../data/clientes.csv', sep=';')
df_produtos = pd.read_csv('../../data/produtos.csv', sep=';')
df_transacoes = pd.read_csv('../../data/transacoes.csv', sep=';')
df_transacao_produto = pd.read_csv('../../data/transacao_produto.csv', sep=';')


# %%
# 1- Engajamento Máximo: Quantos clientes da base estão inscritos em pelo menos três canais 
# de comunicação diferentes (Email, Twitch, YouTube, BlueSky ou Instagram)?
df_1 = df_clientes.copy()
df_1['total_canais'] = df_1['flEmail'] + df_1['flTwitch'] + df_1['flYouTube'] + df_1['flBlueSky'] + df_1['flInstagram']
clientes_engajados = df_1[df_1['total_canais'] >= 3]
clientes_engajados.shape[0]



# %%
# 2- Tempo de Atualização: Crie uma coluna no DataFrame de clientes mostrando quantos
# dias se passaram entre a DtCriacao da conta e a DtAtualizacao. Quais são os 5 clientes
# que demoraram mais tempo para atualizar o cadastro?
df_clientes['DtCriacao'] = pd.to_datetime(df_clientes['DtCriacao'])
df_clientes['DtAtualizacao'] = pd.to_datetime(df_clientes['DtAtualizacao'])
df_clientes['DiasPas'] = (df_clientes['DtAtualizacao'] - df_clientes['DtCriacao']).dt.days
top_cli= df_clientes.sort_values(by='DiasPas', ascending=False).head(5)
top_cli




# %%
# 3- O Fã Clube da Twitch: Usando o que você aprendeu sobre .value_counts() vs .count(), descubra: qual é a 
# categoria de produto (DescCategoriaProduto) mais comprada exclusivamente pelos clientes que têm a flag flTwitch == 1?
df_3 = df_transacao_produto.merge(right=df_produtos, how='inner', on='IdProduto')
df_3 = df_3.merge(right=df_transacoes, how='inner', on='IdTransacao')
df_3 = df_3.merge(right=df_clientes, how='inner', on='IdCliente')
df_3 = df_3[df_3['flTwitch'] == 1]
df_3 = df_3['DescCategoriaProduto'].value_counts().head(1)
df_3



# %%
# 4. Preço Médio da Categoria (Sem Esmagar): Crie uma coluna no df_produtos mostrando o preço médio histórico 
# de venda de cada categoria. 
df_4 = df_produtos.merge(right=df_transacao_produto, how='inner', on='IdProduto')
df_4['preco_medio_categoria'] = df_4.groupby('DescCategoriaProduto')['vlProduto'].transform('mean')
df_medias = df_4[['DescCategoriaProduto', 'preco_medio_categoria']].drop_duplicates()
df_produtos = df_produtos.merge(right=df_medias, on='DescCategoriaProduto', how='left')
df_produtos
# %%
