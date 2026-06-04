# %% 
import pandas as pd

# %% 
df_clientes = pd.read_csv('../../data/clientes.csv', sep=';')
df_produtos = pd.read_csv('../../data/produtos.csv', sep=';')
df_transacoes = pd.read_csv('../../data/transacoes.csv', sep=';')
df_transacao_produto = pd.read_csv('../../data/transacao_produto.csv', sep=';')


# %%
# 1 Filtre a tabela df_transacoes e descubra: quantas transações totais foram realizadas exclusivamente no ano de 2024?
df_transacoes['DtCriacao'] = pd.to_datetime(df_transacoes['DtCriacao'])
filtro_2024 = df_transacoes['DtCriacao'].dt.year == 2024
apenas_2024 = df_transacoes[filtro_2024].shape[0]
print(f"Total de transações em 2024: {apenas_2024}")




# %%
# 2 Descubra quantos clientes (quantidade de IDs únicos na tabela df_clientes) não possuem nenhum registro na tabela df_transacoes.
clientes_sem_compras = df_clientes[~df_clientes['IdCliente'].isin(df_transacoes['IdCliente'])]
total_inativos = clientes_sem_compras['IdCliente'].nunique()
total_inativos



# %%
# 3 Qual produto (DescNomeProduto) foi comprado pelo maior número de clientes diferentes?
df_3 = df_transacao_produto.merge(right=df_produtos, how='inner', on='IdProduto')
df_3 = df_3.merge(right=df_transacoes, how='inner', on='IdTransacao')
qtde_pro = df_3.groupby('DescNomeProduto')['IdCliente'].nunique()
qtde_pro = qtde_pro.sort_values(ascending=False).head(1)
qtde_pro



# %%
# 4 Calcule e compare a receita total gerada pelos clientes que possuem a flag do YouTube (flYouTube == 1) 
# contra a receita total dos clientes que não possuem (flYouTube == 0). Quem trouxe mais dinheiro para a loja?
df_4 = df_clientes.merge(right=df_transacoes, how='inner', on='IdCliente')
df_4 = df_4.merge(right=df_transacao_produto, how='inner', on='IdTransacao')
fl_1 = df_4[df_4['flYouTube'] == 1]
fl_0 = df_4[df_4['flYouTube'] == 0]
receita_1 = fl_1['QtdeProduto'] * fl_1['vlProduto']
receita_1 = receita_1.sum()
receita_0 = fl_0['QtdeProduto'] * fl_0['vlProduto']
receita_0 = receita_0.sum()
print(f"Receita grupo YouTube (1): R$ {receita_1:.2f}")
print(f"Receita grupo Não-YouTube (0): R$ {receita_0:.2f}")
if receita_0 > receita_1:
    print("O grupo SEM YouTube trouxe mais dinheiro.")
else:
    print("O grupo COM YouTube trouxe mais dinheiro.")



# %%
# 5 O time de marketing quer dar 10% de desconto em todos os produtos da categoria "cajado". Olhando para o
#  histórico, se esse desconto já estivesse ativo desde o começo, qual seria a perda financeira exata da loja? 
df_5 = df_transacoes.merge(right=df_transacao_produto, how='inner', on='IdTransacao')
df_5= df_5.merge(df_produtos, how='inner', on='IdProduto')
apenas_cajados = df_5[df_5['DescCategoriaProduto'] == 'cajado']
apenas_cajados = apenas_cajados['QtdeProduto'] * apenas_cajados['vlProduto']
apenas_cajados = apenas_cajados.sum()
perda_financeira = apenas_cajados * 0.10
print(f"A receita atual dos cajados era: R$ {apenas_cajados:.2f}")
print(f"A perda financeira exata com o desconto de 10% seria: R$ {perda_financeira:.2f}")



# %%
# 6 Filtre as vendas apenas da categoria "espada". Em seguida, descubra a receita total de cada compra (IdTransacao)
#  que continha espadas e tire a média geral desses valores.
df_6 = df_transacoes.merge(right=df_transacao_produto, how='inner', on='IdTransacao')
df_6= df_6.merge(df_produtos, how='inner', on='IdProduto')
apenas_espadas = df_6[df_6['DescCategoriaProduto'] == 'espada']
apenas_espadas['total'] = apenas_espadas['QtdeProduto'] * apenas_espadas['vlProduto']
apenas_espadas_total = apenas_espadas.groupby('IdTransacao')['total'].sum()
apenas_espadas_media = apenas_espadas_total.mean()
apenas_espadas_media



# %%
# 7 Usando as tabelas conectadas, liste os IdCliente de quem comprou mais de 10 itens no total (sum de QtdeProduto),
# mas fez isso em 2 ou menos transações distintas (nunique de IdTransacao).
df_7 = df_clientes.merge(df_transacoes, on='IdCliente').merge(df_transacao_produto, on='IdTransacao')
resumo_clientes = df_7.groupby('IdCliente').agg({
    'QtdeProduto': 'sum',      
    'IdTransacao': 'nunique'   
})
filtro = (resumo_clientes['QtdeProduto'] > 10) & (resumo_clientes['IdTransacao'] <= 2)
clientes_focados = resumo_clientes[filtro].index
print(f"Lista de IdClientes que compraram > 10 itens em <= 2 transações:")
print(clientes_focados)
# %%
