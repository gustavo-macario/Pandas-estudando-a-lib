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
# 4. Preço Médio da Categoria: Crie uma coluna no df_produtos mostrando o preço médio histórico 
# de venda de cada categoria. 
df_4 = df_produtos.merge(right=df_transacao_produto, how='inner', on='IdProduto')
df_4['preco_medio_categoria'] = df_4.groupby('DescCategoriaProduto')['vlProduto'].transform('mean')
df_medias = df_4[['DescCategoriaProduto', 'preco_medio_categoria']].drop_duplicates()
df_produtos = df_produtos.merge(right=df_medias, on='DescCategoriaProduto', how='left')
df_produtos




# %%
# 5. Isole em um novo DataFrame apenas as transações que ocorreram no ano de 2025, ordenadas 
# da mais recente para a mais antiga.
df_5 = df_transacoes.copy()
df_5['DtCriacao'] = pd.to_datetime(df_5['DtCriacao'])
df_5 = df_5[df_5['DtCriacao'].dt.year == 2025].copy() 
df_2025_ordenado = df_5.sort_values(by='DtCriacao', ascending=False)
df_2025_ordenado



# %%
# 6- Descubra se algum produto em transacao_produto foi vendido por um vlProduto diferente em transações distintas.
# Liste o ID desses produtos que tiveram variação de preço.
df_6 = df_transacao_produto.copy()
contagem_precos = df_6.groupby('IdProduto')['vlProduto'].nunique()
produtos_com_variacao = contagem_precos[contagem_precos > 1]
produtos_com_variacao



# %%
# 7- Qual foi o faturamento total (Receita = Quantidade × Valor) gerado por cada DescSistemaOrigem?
df_7 = df_transacao_produto.merge(right=df_transacoes, how='inner', on='IdTransacao')
df_7['total']= df_7['QtdeProduto'] * df_7['vlProduto']
df_7 = df_7.groupby('DescSistemaOrigem')['total'].sum()
df_7



# %%
# 8- Será que existe alguma transação na tabela transacoes que não possui nenhum item registrado na tabela 
# transacao_produto? Descubra fazendo um cruzamento estratégico.
df_8 = df_transacoes.merge(right=df_transacao_produto, how='left', on='IdTransacao')
df_8 = df_8[df_8['IdProduto'].isnull()]
df_8[['IdTransacao', 'DtCriacao', 'IdProduto']]



# %%
# 9- Calcule o "Ticket Médio" de cada cliente. Ou seja: a soma de todo o dinheiro que ele já gastou na loja, 
# dividida pelo número de transações (carrinhos) distintas que ele já fez.
df_9 = df_transacoes.merge(right=df_transacao_produto, how='inner', on='IdTransacao')
df_9['total'] = df_9['QtdeProduto'] * df_9['vlProduto']
df_cliente_consolidado = df_9.groupby('IdCliente').agg(
    faturamento_total = ('total', 'sum'),
    total_carrinhos = ('IdTransacao', 'nunique')
)
df_cliente_consolidado['ticket_medio'] = df_cliente_consolidado['faturamento_total'] / df_cliente_consolidado['total_carrinhos']
df_cliente_consolidado



# %%
# 10 - Para cada cliente que tem mais de uma compra, crie um DataFrame que mostre a data da sua Primeira Compra e a data da sua Última 
# Compra na mesma linha.
df_10 = df_transacoes.merge(right=df_transacao_produto, how='inner', on='IdTransacao')
df_clientes_compras= df_10.groupby('IdCliente').agg(
    total_compras = ('IdTransacao', 'nunique'),
    pri_compra = ('DtCriacao', 'min'),
    ult_compra = ('DtCriacao', 'max')
)
df_clientes_compras = df_clientes_compras[df_clientes_compras['total_compras']> 1]
df_clientes_compras



# %%
# 11- Crie um gráfico imaginário de crescimento! Calcule a soma cumulativa da receita da loja ao longo do tempo, dia após dia,
# unindo todas as vendas cronologicamente.
df_11 = df_transacoes.merge(right=df_transacao_produto, how='inner', on='IdTransacao')
df_11['data'] = pd.to_datetime(df_11['DtCriacao']).dt.date
df_11['total'] = df_11['QtdeProduto'] * df_11['vlProduto']
faturamento_diario =  df_11.groupby('data')['total'].sum().sort_index()
crescimento_global = faturamento_diario.cumsum()
crescimento_global



# %%
# 12 - Dos clientes que fizeram mais de uma compra, qual foi o cliente que levou menos tempo (em dias) entre a sua primeira e a sua
# segunda transação? 
df_12 = df_transacoes.copy()
df_12['DtCriacao'] = pd.to_datetime(df_12['DtCriacao'])
df_12 = df_12.sort_values(by=['IdCliente', 'DtCriacao'])

df_12['numero_compra'] = df_12.groupby('IdCliente').cumcount()
df_filtrado = df_12[df_12['numero_compra'].isin([0, 1])].copy()

df_filtrado['dias_proxima_compra'] = df_filtrado.groupby('IdCliente')['DtCriacao'].diff().dt.days

resultado = df_filtrado.sort_values(by='dias_proxima_compra').head(1)
resultado[['IdCliente', 'dias_proxima_compra']]



# %%
# 13 - Crie uma pivot_table cruzando as origens das transações (DescSistemaOrigem nas linhas) e a flag do YouTube (flYouTube nas colunas).
#  Os valores devem ser a contagem de transações únicas. O YouTube traz mais clientes para qual sistema?
df_13 = df_transacoes.merge(right=df_clientes, how='inner', on='IdCliente')
matriz_youtube = pd.pivot_table(
    data= df_13,
    index='DescSistemaOrigem',
    columns='flYouTube',
    values='IdTransacao',
    aggfunc='nunique'
)
matriz_youtube



# %%
# 14- Qual a porcentagem de receita que a categoria que mais vende representa em relação a todo o dinheiro que a loja já 
# fez na história?
df_14 = df_transacao_produto.merge(right=df_produtos, how='inner', on='IdProduto')
df_14['receita_linha'] = df_14['QtdeProduto'] * df_14['vlProduto']
df_14 = df_14[df_14['receita_linha'] > 0]
faturamento_total = df_14['receita_linha'].sum()

faturamento_por_categoria = df_14.groupby('DescCategoriaProduto')['receita_linha'].sum()
maior_faturamento_categoria = faturamento_por_categoria.max()

porcentagem = (maior_faturamento_categoria / faturamento_total) * 100.0
porcentagem



# %%
# 15- Clientes que seguem a loja no Instagram (flInstagram == 1) têm uma média de qtdePontos nas transações maior do 
# que os clientes que não seguem?
df_clientes.groupby('flInstagram')['qtdePontos'].mean().sort_values(ascending=False)
# %%
