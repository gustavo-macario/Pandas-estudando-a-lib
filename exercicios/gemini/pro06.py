# %% 
import pandas as pd

# %% 
df_clientes = pd.read_csv('../../data/clientes.csv', sep=';')
df_produtos = pd.read_csv('../../data/produtos.csv', sep=';')
df_transacoes = pd.read_csv('../../data/transacoes.csv', sep=';')
df_transacao_produto = pd.read_csv('../../data/transacao_produto.csv', sep=';')



# %%
# 1 Calcule e exiba a média, a mediana e o valor máximo da coluna qtdePontos da tabela de clientes
media = df_clientes['qtdePontos'].mean()
mediana = df_clientes['qtdePontos'].median()
maximo = df_clientes['qtdePontos'].max()

print(f"Média de pontos: {media:.2f}")
print(f"Mediana de pontos: {mediana:.2f}")
print(f"Valor máximo: {maximo}")



# %%
# 2 Usando a DtCriacao da tabela de clientes, descubra qual foi o par "Ano-Mês" (ex: 2024-02) que registrou a maior quantidade de contas criadas.
df_clientes['DtCriacao'] = pd.to_datetime(df_clientes['DtCriacao'])
df_clientes['ano_mes'] = df_clientes['DtCriacao'].dt.to_period('M')
ranking_periodos = df_clientes['ano_mes'].value_counts()

periodo_pico = ranking_periodos.index[0]
quantidade_pico = ranking_periodos.iloc[0]

print(f"O pico de cadastros foi em {periodo_pico} com {quantidade_pico} novas contas.")



# %%
# 3 Existe uma diferença entre o que vende mais e o que dá mais dinheiro. Descubra:
# A) Qual DescCategoriaProduto teve a maior quantidade total de itens vendidos (QtdeProduto)?
df_3_a = df_transacao_produto.merge(right=df_produtos, how='inner', on='IdProduto')
quantidade_por_categoria = df_3_a.groupby('DescCategoriaProduto')['QtdeProduto'].sum()
categoria_mais_vendida = quantidade_por_categoria.sort_values(ascending=False).index[0]
categoria_mais_vendida
# %%
# B) Qual DescCategoriaProduto gerou a maior receita financeira total?
df_3_b = df_transacao_produto.merge(right= df_produtos, how='inner', on='IdProduto')
df_3_b['total'] = df_3_b['QtdeProduto'] * df_3_b['vlProduto']
df_3_b = df_3_b.groupby('DescCategoriaProduto')['total'].sum()
df_3_b = df_3_b.sort_values(ascending=False)
df_3_b.index[0]



# %%
# 4 Agrupe a tabela transacao_produto por IdTransacao para descobrir o valor total de cada compra. Em seguida, 
# calcule a média geral desses valores. Qual é o ticket médio da loja?
df_4 = df_transacao_produto.copy()
df_4['total'] = df_4['QtdeProduto'] * df_4['vlProduto']
compras_fechadas = df_4.groupby('IdTransacao')['total'].sum()
ticket_medio = compras_fechadas.mean()
print(f"O ticket médio da loja é: R$ {ticket_medio:.2f}")



# %%
# 5 Usando a tabela transacoes, calcule a média de pontos gerados por transação, comparando o sistema de origem 
# "twitch" contra todos os outros sistemas agrupados.
df_5 = df_transacoes.copy()
df_5_twitch = df_5[df_5['DescSistemaOrigem']=='twitch']
df_5_twitch_media = df_5_twitch['QtdePontos'].mean()
df_5_outros = df_5[df_5['DescSistemaOrigem'] != 'twitch']
df_5_outros = df_5_outros['QtdePontos'].mean()
print(f"Média de pontos gerados via Twitch: {df_5_twitch_media:.2f}")
print(f"Média de pontos gerados via Outros Sistemas: {df_5_outros:.2f}")



# %%
# 6 Na tabela de clientes, calcule a diferença em dias entre a DtAtualizacao e a DtCriacao. Qual é o tempo médio (em dias) 
# que os clientes demoram para atualizar o perfil após a criação?
df_6 = df_clientes.copy()
df_6['DtAtualizacao'] = pd.to_datetime(df_6['DtAtualizacao'])
df_6['DtCriacao'] = pd.to_datetime(df_6['DtCriacao'])
diff_dias = df_6['DtAtualizacao'] - df_6['DtCriacao'] 
media= diff_dias.mean()
print(f"O tempo médio que os clientes demoram para atualizar o perfil é de: {media.days} dias.")



# %%
# 7 Crie um filtro para dividir os clientes em dois grupos: os que possuem 2 ou mais redes sociais vinculadas 
# (soma das flags de redes) e os que possuem 1 ou nenhuma. Qual dos dois grupos gerou a maior receita total histórica para a loja?
df_7 = df_clientes.merge(right=df_transacoes, how='inner', on='IdCliente')
df_7 = df_7.merge(right=df_transacao_produto, how='inner', on='IdTransacao')
df_7['total'] = df_7['QtdeProduto'] * df_7['vlProduto']
df_7['qtde_redes'] = df_7['flTwitch'] + df_7['flYouTube'] + df_7['flBlueSky'] + df_7['flInstagram']
df_2_mais = df_7[df_7['qtde_redes'] >= 2]
df_1_menos = df_7[df_7['qtde_redes'] <= 1]
total_2_mais = df_2_mais['total'].sum()
total_1_menos = df_1_menos['total'].sum()
if total_2_mais > total_1_menos:
    print(f"O grupo com 2+ redes sociais gerou a MAIOR receita: R$ {total_2_mais:.2f}")
else:
    print(f"O grupo com 1 ou menos redes gerou a MAIOR receita: R$ {total_1_menos:.2f}")



# %%
# 8 Gere uma tabela que mostre, para cada categoria de produto (DescCategoriaProduto), o preço mínimo, 
# o preço máximo e o preço médio unitário (vlProduto) praticado nas transações.
df_8 = df_transacao_produto.merge(right=df_produtos, how='inner', on='IdProduto')
tabela_precos = df_8.groupby('DescCategoriaProduto')['vlProduto'].agg(['min', 'max', 'mean']).reset_index()
tabela_precos



# %%
# 9 Descubra quem são os Top 10 clientes que mais gastaram dinheiro na loja (maior receita total). Em seguida, 
# calcule: qual é a porcentagem que esses 10 clientes representam sobre o faturamento total e absoluto da loja?
df_9 = df_transacao_produto.merge(right=df_transacoes, how='inner', on='IdTransacao')
df_9['total'] = df_9['QtdeProduto'] * df_9['vlProduto']
total_cliente = df_9.groupby('IdCliente')['total'].sum()
total_cliente = total_cliente.sort_values(ascending=False).head(10).sum()
total = df_9['total'].sum()
porc_clientes = (total_cliente / total) * 100.0
porc_clientes



# %%
# 10 Encontre o cliente que possui o maior número de transações distintas (Frequência). Se houver empate, 
# o critério de desempate será a receita total gerada (Valor Monetário). Exiba o IdCliente desse "MVP".
df_10 = df_transacao_produto.merge(right=df_transacoes, how='inner', on='IdTransacao')
df_10['total'] = df_10['QtdeProduto'] * df_10['vlProduto']
resumo_mvp = df_10.groupby('IdCliente').agg({
    'IdTransacao': 'nunique', 
    'total': 'sum'            
}).reset_index()
resumo_mvp.columns = ['IdCliente', 'Frequencia', 'ReceitaTotal']
resumo_ordenado = resumo_mvp.sort_values(
    by=['Frequencia', 'ReceitaTotal'], 
    ascending=[False, False] 
)
cliente_mvp = resumo_ordenado.iloc[0]['IdCliente']
print(f"O grande cliente MVP da loja é o ID: {cliente_mvp}")
# %%
