# %%
import pandas as pd
import numpy as np

np.random.seed(42)

df_clientes = pd.DataFrame({
    'id_cliente': range(1, 51),
    'estado': np.random.choice(['SP', 'RJ', 'MG', 'RS', 'PR', 'SC', 'BA', 'PE'], 50),
    'segmento': np.random.choice(['Varejo', 'Atacado'], 50, p=[0.75, 0.25])
})

df_produtos = pd.DataFrame({
    'id_produto': [101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115],
    'nome_produto': ['Smartphone X', 'Notebook Pro', 'Smart TV 55', 'Ar Condicionado', 'Geladeira Duplex',
                     'Monitor 27', 'Teclado Mecânico', 'Mouse Sem Fio', 'Cadeira Ergonomica', 'Mesa de Escritório',
                     'Fone Bluetooth', 'Caixa de Som', 'Tablet 10', 'Smartwatch', 'Console Videogame'],
    'categoria': ['Mobile', 'Informática', 'Eletrônicos', 'Eletrodomésticos', 'Eletrodomésticos',
                  'Informática', 'Periféricos', 'Periféricos', 'Móveis', 'Móveis',
                  'Acessórios', 'Acessórios', 'Mobile', 'Acessórios', 'Eletrônicos'],
    'preco_venda': [2500, 4500, 3200, 1800, 3500, 1200, 350, 150, 900, 600, 200, 400, 1500, 800, 4000],
    'custo_unidade': [1500, 3000, 2100, 1100, 2300, 800, 150, 60, 500, 300, 80, 180, 900, 400, 2800]
})

datas = pd.date_range(start='2023-01-01', end='2023-12-31', freq='D')
df_pedidos = pd.DataFrame({
    'id_pedido': range(1001, 1501),
    'id_cliente': np.random.choice(df_clientes['id_cliente'], 500),
    'id_produto': np.random.choice(df_produtos['id_produto'], 500),
    'data_compra': np.random.choice(datas, 500),
    'quantidade': np.random.randint(1, 6, 500),
    'status': np.random.choice(['Concluído', 'Cancelado', 'Em Trânsito', np.nan], 500, p=[0.70, 0.15, 0.10, 0.05])
})
df_pedidos['data_compra'] = pd.to_datetime(df_pedidos['data_compra'])


# %%
# 1 (Limpeza de Dados): "Notei que o sistema falhou e alguns pedidos vieram sem informação na coluna status.
# Descubra quantos são. Assuma que foi erro de integração e preencha todos esses espaços vazios com a palavra 'Concluído'."
pedidos_sem_info = df_pedidos['status'].isna().sum()
df_pedidos['status'] = df_pedidos['status'].fillna('Concluído')
df_pedidos



# %%
# 2 (Base Útil): "Nós não faturamos pedidos cancelados. Crie um novo DataFrame chamado df_vendas_validas que contenha apenas os
#  pedidos com status 'Concluído' ou 'Em Trânsito'. Traga também as informações do Produto para dentro dessa tabela. Quantas
#  linhas sobraram?"
df_vendas_validas = df_pedidos.copy()
status_validos = ['Concluído', 'Em Trânsito']
df_vendas_validas = df_pedidos[df_pedidos['status'].isin(status_validos)].copy()
df_vendas_validas = df_vendas_validas.merge(right=df_produtos, how='inner', on='id_produto')
print(f'Sobraram {len(df_vendas_validas)} linhas.')


# %%
# 3 (Receita e Custo): "No df_vendas_validas, calcule a Receita Total de cada linha e o Custo Total de cada linha. Salve isso em duas novas colunas."
df_vendas_validas['receita_total'] = df_vendas_validas['preco_venda'] * df_vendas_validas["quantidade"]
df_vendas_validas['custo_total'] = df_vendas_validas['custo_unidade'] * df_vendas_validas["quantidade"]
df_vendas_validas


# %%
# 4 (Métrica de Margem): "Qual é a nossa Margem de Lucro Geral do ano? Imprima o resultado com duas casas decimais."
soma_receita = (df_vendas_validas['preco_venda'] * df_vendas_validas['quantidade']).sum()
soma_custo = (df_vendas_validas['custo_unidade'] * df_vendas_validas['quantidade']).sum()

margem_lucro = ((soma_receita - soma_custo) / soma_receita) * 100

print(f'Nossa margem de lucro é de {margem_lucro:.2f}%')


# %%
# 5 (Sazonalidade): "Quero saber como foi o nosso desempenho financeiro ao longo do ano. Me mostre a Receita Total somada por mês.
#  Qual foi o melhor mês da empresa?"
df_vendas_validas['mes'] = df_vendas_validas['data_compra'].dt.month
receitas_mes = df_vendas_validas.groupby('mes')['receita_total'].sum().sort_values(ascending=False).head(1)
print(f'O melhor mes da empresa foi o {receitas_mes.index[0]}')


# %%
# 6 (Segmentação de Público): "Precisamos cruzar os dados dos pedidos válidos com a tabela de clientes. Quero saber o total de
#  Receita gerado pelo segmento 'Varejo' versus o segmento 'Atacado'."
df_6 = df_pedidos.copy()
df_6 = df_6[df_6['status'].isin(['Concluído', 'Em Trânsito'])]
df_6 = df_6.merge(right=df_clientes, how='inner', on='id_cliente')
df_6 = df_6.merge(right=df_produtos, how='inner', on='id_produto')

df_6['receita'] = df_6['quantidade'] * df_6['preco_venda']

receita_por_segmento = df_6.groupby('segmento')['receita'].sum()
print(receita_por_segmento)


# %%
# 7 (Ticket Médio por Categoria): "O Marketing quer investir em tráfego pago. Calcule o Ticket Médio de cada Categoria de produto. Qual categoria tem o maior ticket médio?
df_7 = df_pedidos.copy()
df_7 = df_7.merge(right=df_produtos, how='inner', on='id_produto')
df_7['receita_pedido'] = df_7['preco_venda'] * df_7['quantidade']
resumo = df_7.groupby('categoria')['receita_pedido'].agg(
    soma_receita= 'sum',
    qtde_pedidos='count'
)
resumo['ticket_medio'] = (resumo['soma_receita'] / resumo['qtde_pedidos'])
campeao = resumo.sort_values(by='ticket_medio', ascending=False)
print(f"A categoria com maior ticket médio é: {campeao.index[0]}")


# %%
# 8 (Ranking de Produtos): "A equipe de logística pediu um relatório de volume de caixas. Liste os produtos em ordem decrescente
# baseada na quantidade total de unidades vendidas. Qual foi o campeão de vendas em volume físico?"
df_8 = df_pedidos.copy()
df_8 = df_8.merge(right=df_produtos, how='inner', on='id_produto')
unidades_vendidas = df_8.groupby('nome_produto')['quantidade'].sum().sort_values(ascending=False)
print(f'O campeao de vendas foi: {unidades_vendidas.index[0]}, com {unidades_vendidas.values[0]} vendas.')


# %%
# 9 (Análise de Recorrência - Clientes Fiéis): "Quantos clientes compraram com a gente mais de uma vez ao longo do ano? 
# (Considere apenas as vendas válidas e conte quantos id_cliente aparecem mais de uma vez na tabela). Me diga o número total 
# de clientes recorrentes."
df_9 = df_vendas_validas.copy()
pedidos_por_cliente = df_9.groupby('id_cliente').size()
total_recorrentes = (pedidos_por_cliente > 1).sum()
print(f"Total de clientes recorrentes: {total_recorrentes}")


# %%
# 10 (Visão Executiva - O Mapa do Faturamento): "Para a reunião de diretoria, preciso de uma visão cruzada. Quero uma tabela 
# onde as linhas sejam os Estados (UF), as colunas sejam as Categorias de produtos, e os valores no meio sejam a Soma da Receita Total.
# Onde não houver venda, o sistema deve mostrar 0 em vez de nulo (NaN)."
df_10 = df_vendas_validas.copy()
df_10 = df_10.merge(right=df_clientes, how='inner', on='id_cliente')
tabela_executiva = pd.pivot_table(
    data= df_10,
    index= 'estado',
    columns= 'categoria',
    values= 'receita_total',
    aggfunc= sum,
    fill_value= 0
).round(2)
tabela_executiva
# %%
