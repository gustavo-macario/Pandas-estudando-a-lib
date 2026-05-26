# %% 
import pandas as pd

# %% 
df_clientes = pd.read_csv('../../data/clientes.csv', sep=';')
df_produtos = pd.read_csv('../../data/produtos.csv', sep=';')
df_transacoes = pd.read_csv('../../data/transacoes.csv', sep=';')
df_transacao_produto = pd.read_csv('../../data/transacao_produto.csv', sep=';')


# %%
# 1. Safra Específica: Descubra quantas transações (df_transacoes) foram feitas apenas por clientes criados
#  (DtCriacao do df_clientes) no ano de 2026.
df_clientes['DtCriacao'] = pd.to_datetime(df_clientes['DtCriacao'])
clientes2026 = df_clientes[df_clientes['DtCriacao'].dt.year == 2026]
lista_ids_2026 = clientes2026['IdCliente']
transacoes_safra_2026 = df_transacoes[df_transacoes['IdCliente'].isin(lista_ids_2026)]
transacoes_safra_2026.shape[0]



# %%
# 2. Estoque Parado (Left Join): Existe algum produto no cadastro (df_produtos) que nunca foi vendido na história da loja?
df_pro_vendidos = df_produtos.merge(right=df_transacao_produto, how='left', on=['IdProduto'])
df_pro_nao_vendidos = df_pro_vendidos[df_pro_vendidos['IdTransacao'].isna()]['IdProduto']
df_pro_nao_vendidos



# %%
# 3. Ticket Médio por Categoria: Calcule o valor financeiro médio gasto por compra para cada Categoria de Produto.
df_merge_tp = df_transacao_produto.merge(right=df_produtos, how='inner', on=['IdProduto'])
df_merge_tp['total'] = df_merge_tp['QtdeProduto'] * df_merge_tp['vlProduto']
df_merge_tp = df_merge_tp.groupby('DescCategoriaProduto')['total'].mean()
df_merge_tp



# %%
# 4. O Peso do Cliente (Parte vs. Todo): Crie uma coluna no df_clientes mostrando qual a porcentagem de qtdePontos 
# que aquele cliente tem em relação à soma de pontos de todos os clientes da loja.
total_pontos_loja = df_clientes['qtdePontos'].sum()
df_clientes['Pct_Pontos'] = (df_clientes['qtdePontos'] / total_pontos_loja) * 100
df_clientes[['IdCliente', 'qtdePontos', 'Pct_Pontos']]



# %%
# 5. Produtos Acima da Média da Sua Categoria: Crie uma flag no df_produtos que diga se o produto é "Mais caro" 
# ou "Mais barato" que a média de preço da categoria dele (e não da loja toda).
df_5 = df_produtos.merge(right=df_transacao_produto, how='inner', on=['IdProduto'])
df_5['media_categoria'] = df_5.groupby('DescCategoriaProduto')['vlProduto'].transform('mean')
import numpy as np
df_5['Flag_Preco'] = np.where(
    df_5['vlProduto'] > df_5['media_categoria'], 
    'Mais caro',
    'Mais barato'
)
df_5[['IdProduto', 'DescCategoriaProduto', 'vlProduto', 'media_categoria', 'Flag_Preco']].drop_duplicates()
df_flags = df_5[['IdProduto', 'Flag_Preco']].drop_duplicates()
df_produtos = df_produtos.merge(right=df_flags, how='left', on='IdProduto')
df_produtos



# %%
# 6. A Cesta de Múltiplas Categorias: Quantos clientes diferentes já compraram produtos de pelo menos
# 3 categorias distintas ao longo da vida? 
df_6 = df_transacoes.merge(right=df_transacao_produto, how='inner', on=['IdTransacao'])
df_6 = df_6.merge(right=df_produtos, how='inner', on=['IdProduto'])
df_6 = df_6.groupby('IdCliente')['DescCategoriaProduto'].nunique()
df_6 = df_6[df_6 >= 3].count()
df_6



# %%
# 7. Participação no Carrinho (Desafio Clássico): No DataFrame df_transacao_produto, crie uma coluna
#  mostrando qual a porcentagem (%) do valor daquele item em relação ao valor total daquela transação 
# específica.
df_transacao_produto['total_item'] = df_transacao_produto['QtdeProduto'] * df_transacao_produto['vlProduto']
df_transacao_produto['total_carrinho'] = df_transacao_produto.groupby('IdTransacao')['total_item'].transform('sum')
df_transacao_produto['porc_participacao'] = (df_transacao_produto['total_item'] / df_transacao_produto['total_carrinho']) * 100

df_transacao_produto



# %%
# 8. Matriz de Fidelidade vs. Origem: Usando a coluna de Ouro/Prata/Bronze que você criou antes, gere uma pivot_table 
# que mostre a soma de receita cruzando Categoria de Fidelidade (linhas) e Sistema de Origem (colunas).
df_total_pontos = df_clientes.groupby('IdCliente')['qtdePontos'].sum()
df_total_pontos = df_total_pontos.sort_values(ascending=False)
df_clientes['Categoria_Fidelidade'] = pd.qcut(
    df_clientes['qtdePontos'], 
    q=3, 
    labels=['Bronze', 'Prata', 'Ouro']
)

df_8 = df_clientes.merge(right=df_transacoes, how='inner', on=['IdCliente'])
df_8 = df_8.merge(right=df_transacao_produto, how='inner', on=['IdTransacao'])
df_8['receita'] = df_8['QtdeProduto'] * df_8['vlProduto'] 

df_matriz = pd.pivot_table(
    data=df_8,
    index='Categoria_Fidelidade',    
    columns='DescSistemaOrigem',       
    values='receita',                 
    aggfunc='sum',           
    fill_value=0                             
)
df_matriz




# %%
# 9. Tempo até a Segunda Compra: Para os clientes que têm mais de 1 compra, calcule quantos dias, em média, eles 
# levaram entre a primeira e a segunda compra.
df_9 = df_transacoes['DtCriacao'] = pd.to_datetime(df_transacoes['DtCriacao'])
df_9 = df_transacoes.sort_values(by='DtCriacao').copy()
df_9['Num_Compra'] = df_9.groupby('IdCliente').cumcount()
df_9['Data_Anterior'] = df_9.groupby('IdCliente')['DtCriacao'].shift(1)
df_9['Dias_Desde_Anterior'] = (df_9['DtCriacao'] - df_9['Data_Anterior']).dt.days
df_segunda_compra = df_9[df_9['Num_Compra'] == 1]
resultado_final = df_segunda_compra['Dias_Desde_Anterior'].mean()
resultado_final



# %%
# 10. Clientes Inativos: Descubra quantos clientes não fazem uma transação há mais de 60 dias 
# (considerando a data da transação mais recente de cada um).
df_transacoes['DtCriacao'] = pd.to_datetime(df_transacoes['DtCriacao'])
df_10 = df_transacoes.sort_values(by='DtCriacao', ascending=False).copy()
df_10['Num_Compra'] = df_10.groupby('IdCliente').cumcount()
df_ultimas_compras = df_10[df_10['Num_Compra'] == 0].copy()
df_ultimas_compras['dias_ult'] = (pd.Timestamp.now() - df_ultimas_compras['DtCriacao']).dt.days
df_resultado = df_ultimas_compras[df_ultimas_compras['dias_ult'] > 60]
df_resultado



# %%
# 11. Sazonalidade de Categoria: Descubra qual mês/ano teve a maior quantidade vendida da categoria 
# que a loja mais vende no geral.
df_11 = df_transacao_produto.merge(right=df_produtos, how='inner', on=['IdProduto'])
df_11['total'] = df_11['QtdeProduto'] * df_11['vlProduto']
df_11 = df_11.groupby('DescCategoriaProduto')['total'].sum()
df_11 = df_11.sort_values(ascending=False).head(1)
df_sazonalidade = df_transacao_produto.merge(right=df_produtos, on='IdProduto', how='inner')
df_sazonalidade = df_sazonalidade.merge(right=df_transacoes, on='IdTransacao', how='inner')


df_campea = df_sazonalidade[df_sazonalidade['DescCategoriaProduto'] == 'present'].copy()
df_campea['DtCriacao'] = pd.to_datetime(df_campea['DtCriacao'])
df_campea['Ano_Mes'] = df_campea['DtCriacao'].dt.to_period('M')
resultado = df_campea.groupby('Ano_Mes')['QtdeProduto'].sum().sort_values(ascending=False)
resultado.head(1)



# %%
# 12. Receita Acumulada por Origem: Faça a soma cumulativa da receita da loja ao longo do tempo, mas crie
#  linhas separadas para acompanhar o crescimento do faturamento do Sistema A, Sistema B, etc.
df_12 = df_transacao_produto.merge(right=df_transacoes, how='inner', on='IdTransacao')
df_12['total'] = df_12['QtdeProduto'] * df_12['vlProduto']
df_12 = df_12.sort_values(by='DtCriacao').copy()
df_12['acumulado'] = df_12.groupby('DescSistemaOrigem')['total'].cumsum()
df_12



# %%
# 13. Top 3 Histórico: Quais são os 3 produtos específicos (Id e Nome) que mais geraram receita absoluta na
# história da loja?
df_13 = df_transacao_produto.merge(right=df_produtos, how='inner', on='IdProduto')
df_13['total'] = df_13['QtdeProduto'] * df_13['vlProduto']
faturamento_por_produto = df_13.groupby(['IdProduto', 'DescNomeProduto'])['total'].sum()
faturamento_por_produto = faturamento_por_produto.sort_values(ascending=False).head(3)
faturamento_por_produto



# %%
# 14. Filtro de "Baleias": Crie um DataFrame (df_baleias) contendo todas as linhas do master 
# correspondentes apenas às transações (carrinhos) que ultrapassaram o valor total de R$ 1.000,00.
df_master = df_transacao_produto.merge(right=df_produtos, how='inner', on='IdProduto')
df_master = df_master.merge(right=df_transacoes, how='inner', on='IdTransacao')
df_master = df_master.merge(right=df_clientes, how='inner', on='IdCliente')
df_master['total'] = df_master['QtdeProduto'] * df_master['vlProduto']
df_master['total_carrinho'] = df_master.groupby('IdTransacao')['total'].transform('sum')
df_baleias = df_master[df_master['total_carrinho'] > 1000]
df_baleias



# %%
# 15. A Primeira Escolha: Qual é a categoria de produto mais comum que aparece na primeira 
# transação da vida de um cliente? (Dica: Ordene por data, use drop_duplicates mantendo a 
# primeira compra, e depois conte as categorias).
df_15= df_transacao_produto.merge(right=df_transacoes, how='inner', on='IdTransacao')
df_15= df_15.merge(right=df_produtos, how='inner', on='IdProduto')
df_15 = df_15.sort_values(by='DtCriacao')
df_15 = df_15.drop_duplicates(subset='IdCliente', keep='first').copy()
resultado = df_15['DescCategoriaProduto'].value_counts().head(1)
resultado
# %%
    