# %%
import pandas as pd
import numpy as np

np.random.seed(100)

cidades = ['Ribeirão Preto', 'Piracicaba', 'Campinas', 'Bauru', 'Franca']
df_produtores = pd.DataFrame({
    'id_produtor': range(1, 41),
    'nome': [f'Produtor_{i}' for i in range(1, 41)],
    'cidade': np.random.choice(cidades, 40),
    'hectares': np.random.randint(10, 500, 40),
    'certificacao_organica': np.random.choice([True, False], 40, p=[0.3, 0.7])
})

df_culturas = pd.DataFrame({
    'id_cultura': range(101, 111),
    'nome_cultura': ['Soja', 'Milho', 'Café', 'Laranja', 'Tomate', 'Alface', 'Manga', 'Feijão', 'Cenoura', 'Morango'],
    'tipo': ['Grão', 'Grão', 'Grão', 'Fruta', 'Hortaliça', 'Hortaliça', 'Fruta', 'Grão', 'Hortaliça', 'Fruta'],
    'preco_kg_base': [2.5, 1.2, 15.0, 0.8, 3.5, 2.0, 4.0, 5.0, 1.5, 12.0]
})

datas = pd.date_range(start='2023-01-01', end='2023-12-31', freq='D')
df_producao = pd.DataFrame({
    'id_registro': range(1000, 1600),
    'id_produtor': np.random.choice(df_produtores['id_produtor'], 600),
    'id_cultura': np.random.choice(df_culturas['id_cultura'], 600),
    'data_colheita': np.random.choice(datas, 600),
    'quantidade_kg': np.random.randint(100, 5000, 600),
    'qualidade': np.random.choice(['A', 'B', 'C', np.nan], 600, p=[0.4, 0.3, 0.2, 0.1])
})
df_producao['data_colheita'] = pd.to_datetime(df_producao['data_colheita'])

# %%
# Q1: A diretoria quer focar em grandes produtores sustentáveis. Identifique e imprima apenas os nomes dos produtores da cidade de 
# 'Ribeirão Preto' que possuem propriedades com mais de 100 hectares E que possuem certificação orgânica.
filtro =df_produtores[(df_produtores['cidade'] == 'Ribeirão Preto') & (df_produtores['hectares'] > 100) & (df_produtores['certificacao_organica'] == True)]
print(filtro['nome'])


# %%
# Q2: Os fiscais esqueceram de classificar a qualidade de algumas colheitas (valores nulos na tabela de produção). Assuma o cenário mais
# conservador e preencha todos esses espaços vazios com a classificação 'C'. Em seguida, calcule a quantidade total (soma de kg) produzida 
# exclusivamente com qualidade 'A' no ano inteiro.
df_producao['qualidade'] = df_producao['qualidade'].replace(['NaN', 'nan'], np.nan)
df_producao['qualidade'] = df_producao['qualidade'].fillna('C')
df_2 = df_producao[df_producao['qualidade'] == 'A']
soma_total = df_2['quantidade_kg'].sum()
print(f"Total produzido de qualidade A: {soma_total:,} kg")


# %%
# Q3: Qual é o volume físico total produzido pela associação dividido por cada tipo macro de cultura (Grão, Fruta, Hortaliça)?
df_3 = df_producao.merge(right=df_culturas, how='inner', on='id_cultura')
volume_fisico = df_3.groupby('tipo')['quantidade_kg'].sum() 
volume_fisico


# %%
# Q4: Precisamos calcular a Receita Total de cada colheita. Reúna os dados necessários e crie essa coluna. A regra de precificação é: 
# multiplicar a quantidade_kg pelo preco_kg_base. Porém, há uma regra de bônus lógico: Se o produtor possuir certificacao_organica (True)
# E a qualidade da colheita for 'A', o preço base por kg recebe um acréscimo de 30% antes de ser multiplicado pela quantidade.
df_4 = df_producao.merge(right=df_culturas, how='inner', on='id_cultura') 
df_4 = df_4.merge(right=df_produtores, how='inner', on='id_produtor')

condicao = (df_4['certificacao_organica'] == True) & (df_4['qualidade'] == 'A')
preco_final = np.where(condicao, df_4['preco_kg_base'] * 1.30, df_4['preco_kg_base'])
df_4['receita_total'] = df_4['quantidade_kg'] * preco_final
df_4


# %%
# Q5: Considerando a coluna de receita criada na questão anterior, qual foi o mês que concentrou o maior volume financeiro da associação?
df_5 = df_4.copy()
df_5['mes'] = df_5['data_colheita'].dt.month_name()
faturamento_mensal = df_5.groupby('mes')['receita_total'].sum().sort_values(ascending=False)
faturamento_mensal.head(1)


# %%
# Q6: Precisamos premiar os destaques regionais. Para cada cidade, descubra qual foi o produtor (nome) que gerou a maior
# receita total acumulada no ano.
df_6 = df_producao.merge(right=df_culturas, how='inner', on='id_cultura')
df_6 = df_6.merge(right=df_produtores, how='inner', on='id_produtor')
df_6['ano'] = df_6['data_colheita'].dt.year
df_6 = df_6[df_6['ano'] == 2023]
df_6['total'] = df_6['quantidade_kg'] * df_6['preco_kg_base']
receita_total=  df_6.groupby(['cidade', 'nome'])['total'].sum().sort_values(ascending=False).reset_index()
maior_por_cidade = receita_total.groupby('cidade').first().reset_index()
maior_por_cidade


# %%
# Q7: A associação incentiva a diversificação de plantio. Descubra e liste os nomes dos produtores que conseguiram colher, 
# ao longo do ano, pelo menos um produto do tipo 'Fruta' E pelo menos um produto do tipo 'Grão'.
df_7 = df_producao.merge(right=df_culturas, how='inner', on='id_cultura')
df_7 = df_7.merge(right=df_produtores, how='inner', on='id_produtor')
produtores_fruta = set(df_7[df_7['tipo'] == 'Fruta']['nome'])
produtores_grao = set(df_7[df_7['tipo'] == 'Grão']['nome'])

produtores = list(produtores_fruta & produtores_grao)
produtores


# %%
# Q8: O galpão da associação vai escoar toda a produção de 'Soja' acumulada no ano. O frete é feito em carretas bitrem que suportam 
# exatamente 14.000 kg cada. Usando um laço de repetição (simulando o carregamento logístico), descubra quantos caminhões saíram totalmente 
# cheios e quantos kg de Soja sobraram aguardando no armazém.
df_soja = df_producao.merge(df_culturas, on='id_cultura')
df_soja = df_soja[df_soja['nome_cultura'] == 'Soja']

capacidade_caminhao = 14000
caminhoes_cheios = 0
peso_acumulado = 0

for quantidade in df_soja['quantidade_kg']:
    peso_acumulado += quantidade

    while peso_acumulado >= capacidade_caminhao:
        caminhoes_cheios += 1
        peso_acumulado -= capacidade_caminhao

print(f"Caminhões totalmente cheios que saíram: {caminhoes_cheios}")
print(f"Sobra acumulada no armazém: {peso_acumulado} kg")


# %%
# Q9: Crie um dicionário automático via código onde a chave seja a cidade e o valor seja a média de hectares das propriedades daquela 
# região (arredondada para 1 casa decimal).
df_produtores 
medias = df_produtores.groupby('cidade')['hectares'].mean().round(1)
dic = medias.to_dict()
dic


# %%
# Q10: A diretoria de operações solicitou um Mapa Geral de Safra. Crie uma matriz de dados onde as linhas sejam os nomes dos produtores, 
# as colunas sejam os nomes das culturas (Soja, Milho, Manga, etc.), e os valores internos sejam a quantidade total de kg produzidos. 
# Onde um produtor não tiver plantado determinada cultura, o sistema deve exibir o número 0.
df_10 = df_producao.merge(right=df_culturas, how='inner', on='id_cultura')
df_10 = df_10.merge(right=df_produtores, how='inner', on='id_produtor')

resumo = pd.pivot_table(
    data = df_10,
    index='nome',
    columns='nome_cultura',
    values='quantidade_kg',
    aggfunc= 'sum',
    fill_value=0

)
resumo
# %%
