# %%
import pandas as pd
import numpy as np

dados_hardware_v2 = {
    'modelo': ['RTX 4090', 'RTX 3060', 'RX 6700 XT', 'Ryzen 9 7950X', 'Core i5 13400F', 
               '16GB DDR4 3200MHz', '8GB DDR4 2666MHz', 'SSD NVMe 1TB', 'HD 2TB', 
               'Placa Mãe B550', 'Placa Mãe A320', 'Fonte 750W', 'Fonte 500W', 
               'Gabinete ATX', 'Water Cooler 240mm', 'Placa de Rede Wi-Fi', 'SSD SATA 480GB',
               'Monitor 144Hz', 'Monitor 60Hz', 'Mouse Gamer', 'Teclado Mecânico'],
    'categoria': ['Placa de Vídeo', 'Placa de Vídeo', 'Placa de Vídeo', 'Processador', 'Processador', 
                  'Memória RAM', 'Memória RAM', 'Armazenamento', 'Armazenamento', 
                  'Placa Mãe', 'Placa Mãe', 'Fonte', 'Fonte', 
                  'Gabinete', 'Refrigeração', 'Rede', 'Armazenamento',
                  'Monitor', 'Monitor', 'Periféricos', 'Periféricos'],
    'preco': [12000.0, 1800.0, 2200.0, 4000.0, 1200.0, 300.0, 150.0, 450.0, 250.0, 
              800.0, 400.0, 600.0, 300.0, 350.0, 500.0, 120.0, 180.0, 
              1500.0, 600.0, 250.0, 350.0],
    'estoque': [2, 15, 8, 5, 20, 0, 35, 50, 12, 10, 8, 15, 25, 0, 8, 40, 15, 12, 30, 50, 45],
    'score_desempenho': [99, 75, 82, 98, 78, 80, 65, 85, 50, np.nan, 45, 80, np.nan, np.nan, 85, 40, 60, 90, 50, 75, 80] 
}
df_estoque_hardware = pd.DataFrame(dados_hardware_v2)

dados_vendas= {
    'id_venda': [101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112],
    'modelo': ['RTX 3060', 'SSD NVMe 1TB', 'Core i5 13400F', 'RTX 3060', 'Placa Mãe B550', 
               '16GB DDR4 3200MHz', 'Gabinete ATX', 'SSD NVMe 1TB', 'Monitor 144Hz', 
               'Mouse Gamer', 'Teclado Mecânico', 'RX 6700 XT'],
    'quantidade_vendida': [2, 5, 1, 1, 2, 4, 1, 3, 2, 10, 5, 1],
    'data_venda': ['2023-01-15', '2023-01-20', '2023-02-10', '2023-02-25', '2023-03-05', 
                   '2023-03-12', '2023-04-01', '2023-04-15', '2023-05-10', '2023-05-12', 
                   '2023-06-01', '2023-06-20']
}
df_vendas = pd.DataFrame(dados_vendas)
df_vendas['data_venda'] = pd.to_datetime(df_vendas['data_venda'])


# %%
# 1 Filtre e imprima apenas as peças onde o nome da categoria contenha a palavra "Placa" (seja de vídeo, mãe ou rede) 
# E que custem menos de R$ 1.000,00.
df_1 = df_estoque_hardware.copy()
df_1 = df_1[(df_1['preco'] < 1000) & (df_1['categoria'].str.contains('Placa', na=False))]
df_1


# %%
# 2 O DataFrame de hardware tem dados faltantes (NaN). substitua os preços nulos pelo preço médio da tabela 
# inteira, e os scores nulos por 0.
media = df_estoque_hardware['preco'].mean()
df_estoque_hardware['preco'] = df_estoque_hardware['preco'].fillna(media)
df_estoque_hardware['score_desempenho'] = df_estoque_hardware['score_desempenho'].fillna(0)
df_estoque_hardware


# %%
# 3 Usando .loc, aplique 50% de desconto em todos os produtos que tenham estoque maior que 20 unidades.
df_3 = df_estoque_hardware.copy()
df_3.loc[df_3['estoque'] > 20, 'preco'] = df_3['preco'] * 0.50
df_3


# %%
# 4 Crie uma nova coluna no df_estoque_hardware chamada status. Usando .apply(), preencha com "Esgotado" se o estoque for 0, "Baixo" 
# se for menor que 10, e "Normal" para o resto.
def seestatus(estoque):
    if estoque == 0:
        return 'Esgotado'
    elif estoque < 10:
        return 'Baixo'
    else:
        return 'Normal'
    
df_estoque_hardware['status'] = df_estoque_hardware['estoque'].apply(seestatus)
df_estoque_hardware


# %%
# 5 Usando .groupby(), crie um resumo mostrando o preço máximo, o preço mínimo e a soma total do estoque para cada categoria.
df_5 = df_estoque_hardware.copy()
df_5 = df_5.groupby('categoria').agg(
    maximo=('preco', 'max'),
    minimo=('preco', 'min'),
    total_estoque=('estoque', 'sum')
)
df_5


# %%
# 6 Faça um .merge() entre df_vendas e df_estoque_hardware usando a coluna modelo como chave. 
# Salve isso em um novo DataFrame chamado df_vendas_detalhadas.
df_vendas_detalhadas = df_vendas.merge(right=df_estoque_hardware, how='inner', on=['modelo'])
df_vendas_detalhadas 


# %%
# 7 No df_vendas_detalhadas, crie uma coluna receita_total que seja a multiplicação da quantidade_vendida pelo 
# preco da peça. Qual foi a receita total da loja no semestre?
df_vendas_detalhadas['receita_total'] = df_vendas_detalhadas['quantidade_vendida'] * df_vendas_detalhadas['preco']
receita_semestre = df_vendas_detalhadas['receita_total'].sum()
receita_semestre


# %%
# 8 Extraia apenas o mês da coluna data_venda. Depois, use um groupby para descobrir qual mês gerou a maior 
# soma de receita_total.
df_8 = df_vendas_detalhadas.copy()
df_8['mes'] = df_8['data_venda'].dt.month
melhor_mes = df_8.groupby('mes')['receita_total'].sum().sort_values(ascending=False)
print(f"O mês que gerou a maior receita foi o mês {melhor_mes.index[0]}!")


# %%
# 9 Use iterrows() no df_estoque_hardware. Crie um dicionário onde a chave seja o modelo e o valor seja o potencial 
# financeiro da peça (preco * estoque). Mas adicione ao dicionário apenas as peças com score_desempenho >= 80.
df_estoque_hardware
dic = {}
for i, p in df_estoque_hardware.iterrows():
    if p['score_desempenho'] >= 80:
        dic[p['modelo']]= p['preco'] * p['estoque']

dic



# %%
# 10 Você tem R$ 5.000. Crie um laço while que compre 1 unidade da "RTX 3060" repetidamente até o dinheiro acabar OU o estoque zerar. Imprima quantas você comprou e o troco.
saldo = 5000
valor_3060 = df_estoque_hardware.loc  [df_estoque_hardware['modelo'] == 'RTX 3060', 'preco'].values[0]
comprados = 0

while saldo >= valor_3060 and df_estoque_hardware.loc[df_estoque_hardware['modelo'] == 'RTX 3060', 'estoque'].values[0] > 0:
    saldo -= valor_3060
    df_estoque_hardware.loc[df_estoque_hardware['modelo'] == 'RTX 3060', 'estoque'] -= 1
    comprados += 1

print(f"Quantidade comprada: {comprados}")
print(f"Troco: R$ {saldo:.2f}")



# %%
# 11 O gerente determinou uma queima de estoque. Aplique um desconto direto de R$ 100,00 no preço de todos os produtos da categoria 
# "Periféricos" que custem mais de R$ 300,00.
df_estoque_hardware.loc[(df_estoque_hardware['categoria'] == 'Periféricos') & (df_estoque_hardware['preco'] > 300), 'preco'] -= 100
df_estoque_hardware



# %%
# 12 Identifique quais são os 3 produtos mais caros da loja inteira, mas que tenham pelo menos 5 unidades em estoque.
#  Imprima apenas o nome dos modelos e seus preços.
df_12 = df_estoque_hardware.copy()
# df_12 = df_12.sort_values(by='preco', ascending=False)
# df_12.loc[df_12['estoque'] >= 5, ['modelo', 'preco']].head(3)

df_12.loc[df_12['estoque'] >= 5].nlargest(3, 'preco')[['modelo', 'preco']]


# %%
# 13 Elimine da tabela df_estoque_hardware todas as linhas que não possuam avaliação no score_desempenho
# (ou seja, jogue fora os nulos dessa coluna, não preencha com nada). Salve o resultado em um df_limpo.
df_limpo = df_estoque_hardware.copy()
df_limpo = df_limpo.dropna(subset=['score_desempenho'])
df_limpo


# %%
# 14 Crie uma nova coluna chamada custo_beneficio no df_limpo. O cálculo deve ser o score_desempenho dividido pelo preco.
df_limpo['custo_beneficio'] =  df_limpo['score_desempenho'] / df_limpo['preco']
df_limpo['custo_beneficio'] = df_limpo['custo_beneficio'].round(4)
df_limpo


# %%
# 15 Precisamos saber quais produtos são verdadeiras pechinchas. Filtre a tabela para mostrar apenas os produtos cujo preço
# individual seja menor do que a média de preço da sua própria categoria.
df_15 = df_estoque_hardware.copy()
# media_categorias = df_15.groupby('categoria')['preco'].mean()
# df_15 = df_15.merge(right=media_categorias, how='inner', on='categoria')
# df_15 = df_15[df_15['preco_x'] < df_15['preco_y']]

df_15['media'] = df_15.groupby('categoria')['preco'].transform('mean')
pechinchas = df_15[df_15['preco'] < df_15['media']]
pechinchas


# %%
# 16 Junte as tabelas de vendas e estoque. Depois, calcule qual foi a quantidade total de itens vendidos agrupada por Categoria.
df_16 = df_estoque_hardware.merge(right=df_vendas, how='inner', on='modelo')
qtde_total = (df_16.groupby('categoria')['quantidade_vendida'].sum()
              .sort_values(ascending=False).reset_index(name='qtde_vendida'))
qtde_total


# %%
# 17 A contabilidade quer saber o faturamento por período. Calcule a receita total (preço * quantidade) apenas das vendas
# realizadas no primeiro trimestre (meses 1, 2 e 3).
df_17 = df_vendas.copy()
df_17 = df_17.merge(right=df_estoque_hardware, how='inner', on='modelo')
df_17['trimestre'] = df_17['data_venda'].dt.quarter
# receita_total = df_17[df_17['trimestre'] == 1]
# receita_total = (receita_total['preco'] * receita_total['quantidade_vendida']).sum()

df_17['total'] = df_17['preco'] * df_17['quantidade_vendida']
receita_total = df_17.loc[df_17['trimestre'] == 1, 'total'].sum()
print(f"Receita do 1º Trimestre: R$ {receita_total:,.2f}")


# %%
# 18 Identifique todos os produtos na tabela df_estoque_hardware cujo nome do modelo contenha o texto "DDR4" OU contenha a sigla "GB".
df_18 = df_estoque_hardware.copy()
df_18 = df_estoque_hardware.loc[df_estoque_hardware['modelo'].str.contains('DDR4|GB')]
df_18


# %%
# 19 Crie um dicionário onde a chave seja o nome da categoria e o valor seja o potencial financeiro total 
# do estoque daquela categoria.
df_19 = df_estoque_hardware.copy()
dic = {}
df_19['soma'] = df_19['preco'] * df_19['estoque']
# valor_categoria = df_19.groupby('categoria')['soma'].sum()
# for cat, valor in valor_categoria.items():
#     dic[cat] = valor
# dic
dic = df_19.groupby('categoria')['soma'].sum().to_dict()
dic


# %%
# 20 Você recebeu um PIX de R$ 6.000,00 para montar um setup do zero. Compre o máximo de unidades do "Monitor 144Hz" que o dinheiro 
# e o estoque permitirem. Se acabar o estoque do monitor ou o dinheiro não der para mais um, use todo o troco para comprar o máximo
#  possível de "Teclado Mecânico". Mostre a quantidade comprada de cada um e o troco final.
# Maneira 1 
# monitores = df_estoque_hardware[df_estoque_hardware['modelo'].str.contains('144Hz')]
# preco_mon = monitores['preco'].values[0]
# est_monitores = monitores['estoque'].values[0]

# teclados = df_estoque_hardware[df_estoque_hardware['modelo'].str.contains('Teclado Mecânico')]
# est_teclados = teclados['estoque'].values[0]
# preco_tec = teclados['preco'].values[0]

# qtde_tec = 0
# qtde_mon = 0
# saldo = 6000

# while saldo >= preco_mon and est_monitores > 0:
#     est_monitores -= 1
#     saldo -= preco_mon
#     qtde_mon += 1

# while saldo >= preco_tec and est_teclados > 0:
#         est_teclados -= 1
#         saldo -= preco_tec
#         qtde_tec += 1

# print(f'A quantidade total de monitores foi {qtde_mon}, a de teclados foi {qtde_tec}. E o troco final foi {saldo}')

# Maneira 2
monitores = df_estoque_hardware[df_estoque_hardware['modelo'].str.contains('144Hz')]
preco_mon = monitores['preco'].values[0]
est_monitores = monitores['estoque'].values[0]

teclados = df_estoque_hardware[df_estoque_hardware['modelo'].str.contains('Teclado Mecânico')]
preco_tec = teclados['preco'].values[0]
est_teclados = teclados['estoque'].values[0]

saldo = 6000.0

compras_mon = int(saldo // preco_mon)         
qtde_mon = min(compras_mon, est_monitores)    
saldo -= qtde_mon * preco_mon                 

compras_tec = int(saldo // preco_tec)       
qtde_tec = min(compras_tec, est_teclados)   
saldo -= qtde_tec * preco_tec                 

print(f"A quantidade total de monitores foi {qtde_mon}, a de teclados foi {qtde_tec}. E o troco final foi R$ {saldo:,.2f}")
# %%
