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
# 4 Crie uma tabela resumo mostrando, para cada Sistema de Origem (DescSistemaOrigem), três métricas simultâneas:
# A quantidade de clientes únicos que compraram por lá.
# O total de itens comprados.
# O ticket médio.
df_4 = df_transacoes.copy()
df_4 = df_4.merge(right=df_transacao_produto, how='inner', on='IdTransacao')
df_4['total'] = df_4['QtdeProduto'] * df_4['vlProduto']
resumo = df_4.groupby('DescSistemaOrigem').agg(
   clientes_unicos=('IdCliente', 'nunique'),
   total_itens=('QtdeProduto', 'sum'),
   ticket_medio=('total', 'mean')
)
resumo


# %%
# 5 Calcule o valor médio, em reais (R$), que os clientes gastam especificamente na sua terceira compra na loja.
# (Desconsidere clientes que compraram menos de 3 vezes).
df_5 = df_transacoes.copy()
df_5 = df_5.merge(right=df_transacao_produto, how='inner', on='IdTransacao')
df_5['DtCriacao'] = pd.to_datetime(df_5['DtCriacao'])
df_5 = df_5.sort_values(by='DtCriacao')
df_5['numeracao_compras'] = df_5.groupby('IdCliente').cumcount()
df_5 = df_5[df_5['numeracao_compras'] == 2]
df_5['total'] = df_5['QtdeProduto'] * df_5['vlProduto']
media = df_5['total'].mean()
media



# %%
# 6 Isole todos os produtos cujo nome comece com a letra "C" (independentemente de ser maiúscula ou minúscula).
# Qual foi a receita financeira histórica total gerada apenas pela venda desses produtos específicos?
df_6 = df_transacao_produto.copy()
df_6 = df_6.merge(right=df_produtos, how='inner', on='IdProduto')
filtro_letra_c = df_6['DescNomeProduto'].str.lower().str.startswith('c')
df_6 = df_6[filtro_letra_c]
df_6['faturamento'] = df_6['QtdeProduto'] * df_6['vlProduto']
receita_total = df_6['faturamento'].sum()
receita_total


# %%
# 7 Extraia uma lista com os IdCliente das pessoas que já compraram itens da categoria "cajado", mas que nunca, 
# em nenhum momento, compraram itens da categoria "espada".
df_7 = df_produtos
df_7 = df_7.merge(right=df_transacao_produto, how='inner', on='IdProduto')
df_7 = df_7.merge(right=df_transacoes, how='inner', on='IdTransacao')
clientes_cajado = df_7[df_7['DescNomeProduto'] == 'cajado']['IdCliente'].unique()
clientes_espada = df_7[df_7['DescNomeProduto'] == 'espada']['IdCliente'].unique()
clientes_filtrados = clientes_cajado[~pd.Series(clientes_cajado).isin(clientes_espada)]
clientes_filtrados


# %%
# 8 Quantos clientes fizeram a sua primeira compra no final de semana (sábado ou domingo) em um prazo menor
# ou igual a 30 dias após terem criado a conta (DtCriacao do cliente)?
df_8 = df_clientes.copy()
df_8 = df_8.merge(right=df_transacoes, how='inner', on='IdCliente')
df_8['DtCriacao_x'] = pd.to_datetime(df_8['DtCriacao_x']) 
df_8['DtCriacao_y'] = pd.to_datetime(df_8['DtCriacao_y']) 
df_8 = df_8.sort_values(by='DtCriacao_y')
df_8['num_compra'] = df_8.groupby('IdCliente').cumcount()
df_primeira_compra = df_8[df_8['num_compra'] == 0].copy()

df_primeira_compra['dias'] = (df_primeira_compra['DtCriacao_y'] - df_primeira_compra['DtCriacao_x']).dt.days
df_primeira_compra = df_primeira_compra[df_primeira_compra['dias'] <= 30]

df_primeira_compra['dia_semana'] = df_primeira_compra['DtCriacao_y'].dt.weekday

df_final = df_primeira_compra[df_primeira_compra['dia_semana'] >= 5]

quantidade_clientes = df_final.shape[0]

print(f"Total de clientes que atenderam às condições: {quantidade_clientes}")


# %%
# 9 Crie uma tabela que liste TODOS os clientes da base e o total financeiro que eles já gastaram na loja. Para os 
# clientes que nunca gastaram nada, a coluna de total gasto deve mostrar 0.0 (em vez de NaN). Ordene a tabela do cliente 
# que mais gastou para o que menos gastou.
df_9 = df_clientes.copy()
df_9 = df_9.merge(right=df_transacoes, how='left', on='IdCliente')
df_9 = df_9.merge(right=df_transacao_produto, how='left', on='IdTransacao')
df_9['total_gasto'] = df_9['QtdeProduto'] * df_9['vlProduto']
total = df_9.groupby('IdCliente')['total_gasto'].sum()
total = total.sort_values(ascending=False)
total = total.fillna(0)
total



# %%
# 10 Encontre o IdCliente do usuário "Mestre da Loja". Ele atende a estas três condições simultaneamente:
# Possui mais de 100 dias de "tempo de vida" na loja (diferença entre a data da sua primeira transação e da sua última 
# transação).     
# Já comprou produtos de pelo menos 3 categorias (DescCategoriaProduto) diferentes.
# O valor da sua última compra foi maior que o valor da sua primeira compra.
df_10 = df_clientes.copy()

df_10 = df_10.merge(df_transacoes, on='IdCliente')
df_10 = df_10.merge(df_transacao_produto, on='IdTransacao')
df_10 = df_10.merge(df_produtos, on='IdProduto')

df_10['DtCriacao_y'] = pd.to_datetime(df_10['DtCriacao_y'])

df_10['total_linha'] = df_10['QtdeProduto'] * df_10['vlProduto']

valor_transacao = (
    df_10.groupby(['IdCliente', 'IdTransacao', 'DtCriacao_y'], as_index=False)
         .agg(valor_compra=('total_linha', 'sum'))
)

valor_transacao = valor_transacao.sort_values(
    ['IdCliente', 'DtCriacao_y']
)

resumo = valor_transacao.groupby('IdCliente').agg(
    primeira_data=('DtCriacao_y', 'first'),
    ultima_data=('DtCriacao_y', 'last'),
    valor_primeira_compra=('valor_compra', 'first'),
    valor_ultima_compra=('valor_compra', 'last')
)

categorias = (
    df_10.groupby('IdCliente')['DescCategoriaProduto']
         .nunique()
         .rename('categorias_distintas')
)

resumo = resumo.join(categorias)

condicao_1 = (
    (resumo['ultima_data'] - resumo['primeira_data']).dt.days > 100
)

condicao_2 = (
    resumo['categorias_distintas'] >= 3
)

condicao_3 = (
    resumo['valor_ultima_compra'] >
    resumo['valor_primeira_compra']
)

mestre_da_loja = resumo[
    condicao_1 &
    condicao_2 &
    condicao_3
]

mestre_da_loja.index
# %%
