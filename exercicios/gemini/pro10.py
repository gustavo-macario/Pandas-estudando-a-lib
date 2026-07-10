 # %%
import pandas as pd

df_clientes = pd.read_csv('../../data/clientes.csv', sep=';')
df_produtos = pd.read_csv('../../data/produtos.csv', sep=';')
df_transacoes = pd.read_csv('../../data/transacoes.csv', sep=';')
df_transacao_produto = pd.read_csv('../../data/transacao_produto.csv', sep=';')

df_clientes['DtCriacao'] = pd.to_datetime(df_clientes['DtCriacao']) 
df_transacoes['DtCriacao'] = pd.to_datetime(df_clientes['DtCriacao']) 


# %%
# 2 Crie uma nova coluna na tabela de clientes chamada NivelEngajamento. A regra de negócio é:
# Se o cliente tiver mais de 10.000 pontos (qtdePontos), ele é "VIP".
# Se tiver entre 1.000 e 10.000 pontos, ele é "Frequente".
# Se tiver menos de 1.000 pontos, ele é "Casual".
def nivel(pontos):
    niveleng = []
    if (pontos > 10000):
         niveleng = 'VIP'
    elif(pontos >= 1000):
        niveleng = 'Frequente'
    else:
          niveleng = 'Casual'
    return niveleng

df_clientes['NivelEngajamento'] = df_clientes['qtdePontos'].apply(nivel)
df_clientes



# %%
# 3 Quantos clientes possuem conta na Twitch (flTwitch == 1) E no YouTube (flYouTube == 1), 
# mas NÃO possuem Instagram (flInstagram == 0)?
df_3 = df_clientes.copy()
df_3 = df_3[(df_3['flTwitch'] == 1) & (df_3['flYouTube'] == 1) & (df_3['flInstagram'] == 0)]
df_3.shape[0]


# %%
# 4 Cruze as transações com os produtos. Qual foi a Receita Total (quantidade * valor) e o Ticket Médio por 
# transação gerados por cada Sistema de Origem (DescSistemaOrigem)?
df_4 = df_transacao_produto.copy()
df_4 = df_4.merge(right=df_transacoes, how='inner', on='IdTransacao')
df_4['total'] = df_4['QtdeProduto'] * df_4['vlProduto']
carrinhos = df_4.groupby(['IdTransacao', 'DescSistemaOrigem'], as_index=False).agg(
     valor_carrinho=('total', 'sum')
)
receita = carrinhos.groupby('DescSistemaOrigem').agg(
     soma_total=('valor_carrinho', 'sum'),
     media=('valor_carrinho', 'mean')
)
receita


# %%
# 5 O time de marketing quer uma visão matricial. Crie uma tabela onde as linhas sejam as Categorias dos Produtos 
# (DescCategoriaProduto),as colunas sejam os Sistemas de Origem (DescSistemaOrigem) e os valores dentro da tabela sejam a 
# quantidade total de itens vendidos.Preencha os valores vazios (NaN) com 0.
# Dica leve: Pesquise sobre pd.pivot_table(). É a versão Pandas da Tabela Dinâmica do Excel.
df_5 = df_transacao_produto.copy()
df_5 = df_5.merge(right=df_transacoes, how='inner', on='IdTransacao')
df_5 = df_5.merge(right=df_produtos, how='inner', on='IdProduto')
tabela_marketing = pd.pivot_table(
     data=df_5,
     index = 'DescCategoriaProduto',
     columns = 'DescSistemaOrigem',
     values= 'QtdeProduto',
     aggfunc = 'sum',
     fill_value = 0
)
tabela_marketing


# %%
# 6 Encontre os 3 produtos que mais geraram faturamento cuja descrição (DescDescricaoProduto) 
# contenha a palavra "fogo" (ignorando maiúsculas e minúsculas).
df_6 = df_transacao_produto.copy()
df_6 = df_6.merge(right=df_transacoes, how='inner', on='IdTransacao')
df_6 = df_6.merge(right=df_produtos, how='inner', on='IdProduto')
df_6 = df_6[df_6['DescDescricaoProduto'].str.contains('fogo', case=False, na=False)]
df_6['total'] = df_6['QtdeProduto'] * df_6['vlProduto']
faturamento = df_6.groupby('IdProduto')['total'].sum()
faturamento = faturamento.sort_values(ascending=False).head(3)
faturamento


# %%
# 7 Qual é o tempo médio, em dias, que os clientes demoram entre a sua primeira e a sua segunda compra?
#  (Desconsidere clientes que compraram apenas uma vez).
df_7 = df_transacoes.copy()
df_7['DtCriacao'] = pd.to_datetime(df_7['DtCriacao'])
df_7 = df_7.sort_values(by='DtCriacao')
df_7['NumCompra'] = df_7.groupby('IdCliente')['DtCriacao'].cumcount()

primeira = df_7[df_7['NumCompra'] == 0][['IdCliente', 'DtCriacao']]
segunda = df_7[df_7['NumCompra'] == 1][['IdCliente', 'DtCriacao']]

recompra = primeira.merge(segunda, on='IdCliente', suffixes=('_1a', '_2a'))
tempo_medio = (recompra['DtCriacao_2a'] - recompra['DtCriacao_1a']).dt.days.mean()
tempo_medio


# %%
# 8 Quantos clientes únicos fizeram compras em pelo menos dois meses diferentes ao longo da história? 
# (Exemplo: comprou em fevereiro e depois voltou a comprar em agosto).
df_8 = df_transacoes.copy()
df_8['DtCriacao'] = pd.to_datetime(df_8['DtCriacao'])
df_8 = df_8.sort_values(by='DtCriacao')
df_8['mes'] = df_8['DtCriacao'].dt.to_period('M')
meses_unicos = df_8.groupby('IdCliente')['mes'].nunique()
meses_unicos = meses_unicos[meses_unicos >= 2]
total_clientes = meses_unicos.shape[0]
total_clientes



# %%
# 9 Liste os IdCliente da elite da loja: aqueles clientes que, somados (do que mais gastou para o que menos gastou),
#  representam os primeiros 50% de todo o faturamento histórico da empresa.
df_9 = df_transacao_produto.copy()
df_9 = df_9.merge(right=df_transacoes, how='inner', on='IdTransacao')
df_9['total'] = df_9['QtdeProduto'] * df_9['vlProduto']
total_cliente = df_9.groupby('IdCliente')['total'].sum()
total_cliente = total_cliente.sort_values(ascending=False)

faturamento_total_loja = total_cliente.sum()
soma_cumulativa = total_cliente.cumsum()

porcentagem_acumulada = soma_cumulativa / faturamento_total_loja
elite = porcentagem_acumulada[porcentagem_acumulada <= 0.50]
elite


# %%
# 10 Encontre a lista de clientes (apenas os IDs) que atendem simultaneamente a estas regras:
# Possuem o nível "VIP" (criado na Questão 2).
# Já compraram pelo menos um item da categoria "espada" E pelo menos um item da categoria "armadura" na mesma vida útil da conta.
# A sua última transação cronológica foi feita pelo sistema de origem "twitch".
df_10 = df_clientes.copy()
df_10 = df_10.merge(right=df_transacoes, how='inner', on='IdCliente')
df_10 = df_10.merge(right=df_transacao_produto, how='inner', on='IdTransacao')
df_10 = df_10.merge(right=df_produtos, how='inner', on='IdProduto')

df_10['DtCriacao_y'] = pd.to_datetime(df_10['DtCriacao_y'])
df_10 = df_10.sort_values(by='DtCriacao_y')

df_10['NivelEngajamento'] = df_10['qtdePontos'].apply(nivel)
df_10 = df_10[df_10['NivelEngajamento'] == 'VIP']

resumo_perfil = df_10.groupby('IdCliente').agg(
    ultimo_canal=('DescSistemaOrigem', 'last'),
    todas_categorias=('DescCategoriaProduto', lambda x: ' '.join(x.unique()))
)

resumo_perfil = resumo_perfil[resumo_perfil['ultimo_canal'] == 'twitch']
condicao_espada = resumo_perfil['todas_categorias'].str.contains('espada', case=False, na=False)
condicao_armadura = resumo_perfil['todas_categorias'].str.contains('armadura', case=False, na=False)
mestre_final = resumo_perfil[condicao_espada & condicao_armadura]
print(mestre_final.index)
# %%
