# %% 
import pandas as pd

# %% 
df_clientes = pd.read_csv('../../data/clientes.csv', sep=';')
df_produtos = pd.read_csv('../../data/produtos.csv', sep=';')
df_transacoes = pd.read_csv('../../data/transacoes.csv', sep=';')
df_transacao_produto = pd.read_csv('../../data/transacao_produto.csv', sep=';')


# %%
# 1 Calcule a média de dias desde a última atualização de cada cliente até a data de hoje. Para clientes com a DtAtualizacao
# nula (faltante), considere a DtCriacao como a data da última atualização.
df_1 = df_clientes.copy()
df_1['DtCriacao'] = pd.to_datetime(df_1['DtCriacao'])
df_1['DtAtualizacao'] = pd.to_datetime(df_1['DtAtualizacao'])
hoje = pd.to_datetime('today')
df_1['DtAtualizacao'] = df_1['DtAtualizacao'].fillna(df_1['DtCriacao'])
df_1['diff_datas'] = hoje - df_1['DtAtualizacao']
media_dias = df_1['diff_datas'].mean().days
media_dias



# %%
# 2 Isole a primeira e a última transação de cada cliente (ordem cronológica). Concatene esses dois recortes em uma única 
# tabela e remova as transações duplicadas (para o caso de clientes que compraram apenas uma vez). Quantas linhas tem o DataFrame 
# final?
df_2 = df_transacoes.copy()
df_2['DtCriacao'] = pd.to_datetime(df_2['DtCriacao'])
df_2 = df_2.sort_values(by='DtCriacao')
primeira = df_2.groupby('IdCliente').first().reset_index()
ultima = df_2.groupby('IdCliente').last().reset_index()
dfs = ([primeira, ultima])
dfs = pd.concat(dfs, ignore_index=True)
dfs= dfs.drop_duplicates()
dfs.shape[0]



# %%
# 3 Crie e aplique uma regra de classificação na tabela de produtos: "Barato" (abaixo de 50), "Médio" 
# (entre 50 e 100) e "Caro" (acima de 100). Qual categoria (DescCategoriaProduto) possui a maior quantidade
#  absoluta de itens "Caros"?
df_3 = df_transacao_produto.merge(right = df_produtos, how='inner', on='IdProduto')
def classificao(p):
    if (p < 50):
        return 'Barato'
    elif(p <= 100):
        return 'Médio'
    else:
        return 'Caro'

df_3['classificacao'] = df_3['vlProduto'].apply(classificao)
df_3



# %%
# 4 Precisamos saber se o canal do YouTube atrai clientes de "bolso mais fundo". Calcule e compare a receita
# total gerada pelos clientes que possuem a flag do YouTube (flYouTube == 1) contra a receita total dos 
# clientes que não possuem (flYouTube == 0). Quem trouxe mais dinheiro para a loja?
df_4 = df_transacao_produto.merge(right = df_transacoes, how='inner', on='IdTransacao')
df_4 = df_4.merge(right = df_clientes, how='inner', on='IdCliente')
df_4['total'] = df_4['QtdeProduto'] * df_4['vlProduto']
clientes_1 = df_4[df_4['flYouTube'] == 1]
clientes_0 = df_4[df_4['flYouTube'] == 0]
total_1 = clientes_1['total'].sum()
total_0 = clientes_0['total'].sum()
if total_1 > total_0:
    print(f"O grupo COM YouTube gerou maior faturamento: R$ {total_1:.2f}")
else:
    print(f"O grupo SEM YouTube gerou maior faturamento: R$ {total_0:.2f}")



# %%
# 5 Quais produtos (exiba os nomes) estão cadastrados na base, mas nunca foram comprados por nenhum cliente?
df_5 = df_produtos.merge(right = df_transacao_produto, how='left', on='IdProduto')
pro_nomes = df_5[df_5['IdTransacao'].isna()]
pro_nomes = pro_nomes['DescNomeProduto'].drop_duplicates()
pro_nomes



# %%
# 6 Utilizando .apply(), crie uma nova coluna no df_produtos contendo os nomes dos produtos sem nenhuma 
# vogal (remova as letras a, e, i, o, u, independentemente do case). Exiba os 5 primeiros resultados.
def remover_vogais(texto):
    vogais = ['a','e', 'i', 'o', 'u', 'A', 'E', 'I', 'O', 'U']
    for v in texto:
       texto = texto.replace(v, "")
    return texto

df_produtos['nomes_s_v'] = df_produtos['DescNomeProduto'].apply(remover_vogais)
df_produtos



# %%
# 7 Para cada cliente (IdCliente), descubra qual foi o IdProduto em que ele mais gastou dinheiro,
# considerando todo o seu histórico de compras somado.
df_7 = df_transacao_produto.merge(right = df_transacoes, how='inner', on='IdTransacao')
df_7['total'] = df_7['QtdeProduto'] * df_7['vlProduto']
df_7 = df_7.groupby(['IdCliente', 'IdProduto'])['total'].sum().reset_index()
gasto_ordenado = df_7.sort_values(by=['IdCliente', 'total'], ascending=[True, False])
produtos_campeoes = gasto_ordenado.groupby('IdCliente').first().reset_index()



# %%
# 8 Qual dia da semana (Segunda, Terça, Quarta...) concentra o maior faturamento histórico geral da loja?
df_8 = df_transacao_produto.merge(right = df_transacoes, how='inner', on='IdTransacao')
df_8['total'] = df_8['QtdeProduto'] * df_8['vlProduto']
df_8['DtCriacao'] = pd.to_datetime(df_8['DtCriacao'])
df_8['dia_semana'] = df_8['DtCriacao'].dt.day_of_week
faturamento_por_dia = df_8.groupby('dia_semana')['total'].sum()
faturamento_por_dia = faturamento_por_dia.sort_values(ascending=False)
dia_campeao = faturamento_por_dia.index[0]
dia_campeao



# %%
# 9 Calcule o tempo médio, em dias, que os clientes demoram entre a sua primeira e a sua segunda transação 
# na loja. (Desconsidere da média os clientes que só possuem uma única compra).
df_9 = df_transacoes.copy()
df_9['DtCriacao'] = pd.to_datetime(df_9['DtCriacao'])
df_9 = df_9.sort_values(by='DtCriacao')
df_9['numero_compra'] = df_9.groupby('IdCliente').cumcount()
df_compra_0 = df_9[df_9['numero_compra'] == 0]
df_compra_1 = df_9[df_9['numero_compra'] == 1]
df_media = df_compra_0.merge(right=df_compra_1, how='inner', on='IdCliente')
df_media['tempo_espera'] = df_media['DtCriacao_y'] - df_media['DtCriacao_x']
tempo_medio_dias = df_media['tempo_espera'].mean().days
print(f"Os clientes demoram, em média, {tempo_medio_dias} dias entre a 1ª e a 2ª compra.")



# %%
# 10 Quantos clientes atendem a todas as seguintes condições simultaneamente:
# Tiveram a conta criada no ano de 2024.
# Possuem 2 ou mais redes sociais diferentes vinculadas.
# Nunca gastaram nenhum centavo na loja (receita total nula/zero).
df_10 = df_clientes.copy()
df_10['DtCriacao'] = pd.to_datetime(df_10['DtCriacao'])
df_10 = df_10[df_10['DtCriacao'].dt.year == 2024]
df_10['total_redes'] = df_10['flTwitch'] + df_10['flYouTube'] + df_10['flBlueSky'] + df_10['flInstagram']
df_10 = df_10[df_10['total_redes'] >= 2]
clientes_compradores = df_transacoes['IdCliente'].unique()
df_10 = df_10[~df_10['IdCliente'].isin(clientes_compradores)]
quantidade_final = df_10.shape[0]
print(f"Quantidade de clientes que atendem a todas as condições: {quantidade_final}")
# %%
