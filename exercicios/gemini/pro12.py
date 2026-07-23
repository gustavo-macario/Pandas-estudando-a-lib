# %%
import pandas as pd
import numpy as np

dados_hardware = {
    'modelo': ['RTX 4090', 'RTX 3060', 'RX 6700 XT', 'Ryzen 9 7950X', 'Core i5 13400F', 
               '16GB DDR4 3200MHz', '8GB DDR4 2666MHz', 'SSD NVMe 1TB', 'HD 2TB', 
               'Placa Mãe B550', 'Placa Mãe A320', 'Fonte 750W', 'Fonte 500W', 
               'Gabinete ATX', 'Water Cooler 240mm', 'Placa de Rede Wi-Fi', 'SSD SATA 480GB'],
    'categoria': ['Placa de Vídeo', 'Placa de Vídeo', 'Placa de Vídeo', 'Processador', 'Processador', 
                  'Memória RAM', 'Memória RAM', 'Armazenamento', 'Armazenamento', 
                  'Placa Mãe', 'Placa Mãe', 'Fonte', 'Fonte', 
                  'Gabinete', 'Refrigeração', 'Rede', 'Armazenamento'],
    'preco': [12000.0, 1800.0, 2200.0, 4000.0, 1200.0, 300.0, 150.0, 450.0, 250.0, 
              800.0, 400.0, 600.0, 300.0, 350.0, 500.0, 120.0, np.nan], 
    'estoque': [2, 15, 8, 5, 20, 0, 35, 50, 12, 10, 8, 15, 25, 0, 8, 40, 15],
    'score_desempenho': [99, 75, 82, 98, 78, 80, 65, 85, 50, np.nan, 45, 80, 60, 50, 85, 40, 60] 
}
df_estoque_hardware = pd.DataFrame(dados_hardware)

dados_vendas = {
    'id_venda': [101, 102, 103, 104, 105, 106, 107, 108],
    'modelo': ['RTX 3060', 'SSD NVMe 1TB', 'Core i5 13400F', 'RTX 3060', 'Placa Mãe B550', '16GB DDR4 3200MHz', 'Gabinete ATX', 'SSD NVMe 1TB'],
    'quantidade_vendida': [2, 5, 1, 1, 2, 4, 1, 3],
    'data_venda': ['2023-01-15', '2023-01-20', '2023-02-10', '2023-02-25', '2023-03-05', '2023-03-12', '2023-04-01', '2023-04-15']
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
