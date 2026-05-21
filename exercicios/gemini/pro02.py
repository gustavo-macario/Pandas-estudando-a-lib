# %% 
import pandas as pd

# %% 
# 1. Importe os 4 arquivos CSV para DataFrames distintos (df_clientes, df_produtos, df_transacoes, df_transacao_produto).
#  Atenção ao delimitador usado nos arquivos.
df_clientes = pd.read_csv('../../data/clientes.csv', sep=';')
df_produtos = pd.read_csv('../../data/produtos.csv', sep=';')
df_transacoes = pd.read_csv('../../data/transacoes.csv', sep=';')
df_transacao_produto = pd.read_csv('../../data/transacao_produto.csv', sep=';')


# %%
# 1. Tempo de Vida do Cadastro
#Crie uma nova coluna no df_clientes chamada Dias_Desde_Atualizacao que calcule a diferença em dias entre a data de 
# hoje e a coluna DtAtualizacao.
df_clientes['DtAtualizacao'] = pd.to_datetime(df_clientes['DtAtualizacao'])
data_hoje = pd.Timestamp.now()
df_clientes['Dias_Desde_Atualizacao'] = (data_hoje - df_clientes['DtAtualizacao']).dt.days
df_clientes



# %%
# 2. Clientes "Fantasmas" (Left Anti-Join)
# Descubra se existe algum cliente na base df_clientes que nunca realizou nenhuma transação 
# (ou seja, não está no df_transacoes).
df_clientes.merge(right=df_transacoes, how='left', on=['IdCliente'])



# %%
# 3. Busca Textual por Palavras-Chave
# No df_produtos, filtre todos os produtos cuja DescDescricaoProduto contenha a palavra "mágico" ou "mágica".
# Garanta que o filtro não seja sensível a letras maiúsculas ou minúsculas (case-insensitive).
filtro = df_produtos['DescDescricaoProduto'].str.contains('mágico|mágica', case=False, na=False)
df_produtos_filtrados = df_produtos[filtro]
df_produtos_filtrados



# %%
# 4. Ticket Médio por Transação
# Usando o df_transacao_produto, agrupe os dados por IdTransacao e calcule o valor total de cada compra (Ticket Médio).
#  Em seguida, descubra qual é a média geral de todas as transações da loja.
df_transacao_produto['ValorTotalItem'] = df_transacao_produto['QtdeProduto'] * df_transacao_produto['vlProduto']
soma_transacao = df_transacao_produto.groupby('IdTransacao')['ValorTotalItem'].sum()
media_transacao = soma_transacao.mean()
media_transacao



# %%
# 5. Resumo do Carrinho (Agregações Múltiplas)
# Ainda com foco no carrinho (IdTransacao), descubra para cada transação: o valor financeiro total e a
# quantidade de produtos distintos comprados nela.
df_transacao_produto.groupby('IdTransacao').agg({'ValorTotalItem' : 'sum',
                                                 'IdProduto': 'count'})




# %%
# 6. Tabela Dinâmica (Pivot Table) de Vendas
# Crie uma visão matricial onde as linhas sejam as categorias dos produtos (DescCategoriaProduto), 
# as colunas sejam os sistemas de origem (DescSistemaOrigem), e os valores no meio da tabela sejam a soma 
# do ValorTotalItem.
df_master = df_produtos.merge(right=df_transacao_produto, how='inner', on='IdProduto')
df_master = df_master.merge(right=df_transacoes, how='inner', on='IdTransacao')
tabela_dinamica = pd.pivot_table(
    data=df_master,
    index='DescCategoriaProduto',
    columns='DescSistemaOrigem',
    values='ValorTotalItem',
    aggfunc='sum',
    fill_value=0
)
tabela_dinamica



# %%
# 7. Sazonalidade de Vendas (Dias da Semana)
# Descubra qual dia da semana (segunda-feira, terça-feira, etc.) possui o maior volume histórico de 
# transações com base na DtCriacao do df_transacoes.
df_transacoes['DtCriacao'] = pd.to_datetime(df_transacoes['DtCriacao'])
df_transacoes['Dia_Nome'] = df_transacoes['DtCriacao'].dt.day_name()
volume_por_dia = df_transacoes.groupby('Dia_Nome')['IdTransacao'].count()
volume_por_dia.sort_values(ascending=False)



# %%
# 8. Segmentação por Quantis (Bronze, Prata, Ouro)
# Crie uma nova coluna no df_clientes chamada Categoria_Fidelidade. Baseado na coluna qtdePontos, divida seus clientes 
# em 3 grupos ("Bronze", "Prata", "Ouro") de forma que a distribuição tente deixar um número parecido de clientes em cada grupo.
df_total_pontos = df_clientes.groupby('IdCliente')['qtdePontos'].sum()
df_total_pontos = df_total_pontos.sort_values(ascending=False)
df_clientes['Categoria_Fidelidade'] = pd.qcut(
    df_clientes['qtdePontos'], 
    q=3, 
    labels=['Bronze', 'Prata', 'Ouro']
)
df_clientes



# %%
# 9. Transação Mais Cara de Cada Cliente (Rankings)
# Descubra qual foi a transação de maior valor financeiro para cada um dos clientes.
valor_por_transacao = df_transacao_produto.groupby('IdTransacao')['ValorTotalItem'].sum().reset_index()
df_com_valor = df_transacoes.merge(valor_por_transacao, on='IdTransacao', how='inner')
df_ordenado = df_com_valor.sort_values(by='ValorTotalItem', ascending=False)
maior_transacao_por_cliente = df_ordenado.drop_duplicates(subset='IdCliente', keep='first')
maior_transacao_por_cliente



# %%
# 10. Precificação Relativa (Abaixo ou Acima da Média)
# Descubra qual é o preço médio global de todos os produtos na loja. Depois, crie uma coluna no df_produtos
#  chamada Faixa_Preco que receba o texto "Acima da Média" se o valor do produto for maior que a média global,
#  e "Abaixo da Média" caso contrário.
import numpy as np
preco_medio_global = df_master['vlProduto'].mean()
df_master['Faixa_Preco'] = np.where(df_master['vlProduto'] > preco_medio_global,
                                      'Acima da Media',
                                      'Abaixo da Media')
df_master




# %%
# 11. Crescimento da Base de Clientes (Análise de Safra/Cohort)
# Agrupe os clientes pelo Ano e Mês de sua DtCriacao e conte quantos clientes novos se cadastraram na loja em
#  cada mês histórico.
df_clientes['DtCriacao'] = pd.to_datetime(df_clientes['DtCriacao'])
df_clientes['Ano/Mes'] = df_clientes['DtCriacao'].dt.to_period('M')
df_clientes.groupby('Ano/Mes')['IdCliente'].count()



# %%
# 12. Clientes Fiéis (Múltiplas Compras)
# Filtre o DataFrame para encontrar apenas os clientes que realizaram mais de 3 transações distintas na 
# loja ao longo da história.
contagem = df_transacoes.groupby('IdCliente')['IdTransacao'].count()
clientes_fieis = contagem[contagem > 3].index  
df_fieis = df_transacoes[df_transacoes['IdCliente'].isin(clientes_fieis)]
df_fieis



# %%
# 13. Market Share das Categorias (% do Total)
# Descubra qual porcentagem (%) da receita total da loja cada categoria de produto (DescCategoriaProduto) 
# representa.
df_pro_tra = df_produtos.merge(right=df_transacao_produto, how='inner', on=['IdProduto'])
df_pro_tra['soma'] = df_pro_tra['QtdeProduto'] * df_pro_tra['vlProduto']
total_por_cat = df_pro_tra.groupby('DescCategoriaProduto')['soma'].sum()
total_loja = total_por_cat.sum()
market_share = (total_por_cat / total_loja) * 100
market_share



# %%
# 14. Deslocamento de Tempo (Frequência de Compra)
# Escolha um cliente específico que tenha feito várias compras. Ordene as compras dele cronologicamente
# e calcule a diferença de dias entre a 2ª compra e a 1ª, a 3ª e a 2ª, etc.
df_cliente_especifico = df_transacoes[df_transacoes['IdCliente'] == '24782f0b-4683-4f35-976a-ea21d6714ba6'].copy()
df_cliente_especifico['DtCriacao'] = pd.to_datetime(df_cliente_especifico['DtCriacao'])
df_cliente_especifico = df_cliente_especifico.sort_values(by='DtCriacao')
df_cliente_especifico['Data_Compra_Anterior'] = df_cliente_especifico['DtCriacao'].shift(1)
df_cliente_especifico['Dias_Entre_Compras'] = (df_cliente_especifico['DtCriacao'] - df_cliente_especifico['Data_Compra_Anterior']).dt.days
df_cliente_especifico[['IdCliente', 'IdTransacao', 'DtCriacao', 'Data_Compra_Anterior', 'Dias_Entre_Compras']]



# %%
# 15. Receita Acumulada no Tempo (Soma Cumulativa)
# Ordene o seu "Master DataFrame" pela data da transação de forma cronológica 
# (do mais antigo ao mais novo). Crie uma coluna mostrando o crescimento do faturamento acumulado 
# dia a dia.
df_master = df_master.sort_values(by='DtCriacao')
df_master['total_acumulado'] = df_master['ValorTotalItem'].cumsum()
df_master
# %%
