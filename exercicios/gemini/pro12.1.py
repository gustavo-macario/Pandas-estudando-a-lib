# %%
import pandas as pd
import numpy as np

dados_hardware_v3 = {
    'modelo': ['RTX 4090', 'RTX 3060', 'RX 6700 XT', 'Ryzen 9 7950X', 'Core i5 13400F', 
               '16GB DDR4 3200MHz', '8GB DDR4 2666MHz', 'SSD NVMe 1TB', 'HD 2TB', 
               'Placa Mãe B550', 'Placa Mãe A320', 'Fonte 750W', 'Fonte 500W', 
               'Gabinete ATX', 'Water Cooler 240mm', 'Placa de Rede Wi-Fi', 'SSD SATA 480GB',
               'Monitor 144Hz', 'Monitor 60Hz', 'Mouse Gamer', 'Teclado Mecânico',
               'Headset 7.1', 'Cadeira Gamer', 'Webcam 1080p'],
    'categoria': ['Placa de Vídeo', 'Placa de Vídeo', 'Placa de Vídeo', 'Processador', 'Processador', 
                  'Memória RAM', 'Memória RAM', 'Armazenamento', 'Armazenamento', 
                  'Placa Mãe', 'Placa Mãe', 'Fonte', 'Fonte', 
                  'Gabinete', 'Refrigeração', 'Rede', 'Armazenamento',
                  'Monitor', 'Monitor', 'Periféricos', 'Periféricos',
                  'Periféricos', 'Móveis', 'Periféricos'],
    'preco_venda': [12000.0, 1800.0, 2200.0, 4000.0, 1200.0, 300.0, 150.0, 450.0, 250.0, 
              800.0, 400.0, 600.0, 300.0, 350.0, 500.0, 120.0, 180.0, 
              1500.0, 600.0, 250.0, 350.0, 400.0, 1200.0, 300.0],
    'custo_fornecedor': [9500.0, 1300.0, 1700.0, 3200.0, 900.0, 180.0, 80.0, 250.0, 120.0,
                         550.0, 250.0, 380.0, 150.0, 200.0, 300.0, 60.0, 90.0,
                         1000.0, 400.0, 100.0, 150.0, 180.0, 700.0, 120.0],
    'estoque': [2, 15, 8, 5, 20, 0, 35, 50, 12, 10, 8, 15, 25, 0, 8, 40, 15, 12, 30, 50, 45, 20, 5, 18],
    'score_desempenho': [99, 75, 82, 98, 78, 80, 65, 85, 50, np.nan, 45, 80, np.nan, np.nan, 85, 40, 60, 90, 50, 75, 80, 70, np.nan, 60] 
}
df_estoque = pd.DataFrame(dados_hardware_v3)

dados_vendas_v3 = {
    'id_venda': [101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115],
    'cliente': ['João', 'Maria', 'João', 'Ana', 'Carlos', 'Maria', 'Pedro', 'Ana', 'João', 'Lucas', 'Ana', 'Carlos', 'Pedro', 'João', 'Maria'],
    'modelo': ['RTX 3060', 'SSD NVMe 1TB', 'Core i5 13400F', 'RTX 3060', 'Placa Mãe B550', 
               '16GB DDR4 3200MHz', 'Gabinete ATX', 'SSD NVMe 1TB', 'Monitor 144Hz', 
               'Mouse Gamer', 'Teclado Mecânico', 'RX 6700 XT', 'Webcam 1080p', 'RTX 3060', 'Monitor 144Hz'],
    'quantidade': [2, 5, 1, 1, 2, 4, 1, 3, 2, 10, 5, 1, 2, -1, 1], # Atenção ao -1 (devolução)!
    'data_venda': ['2023-01-15', '2023-01-20', '2023-02-10', '2023-02-25', '2023-03-05', 
                   '2023-03-12', '2023-04-01', '2023-04-15', '2023-05-10', '2023-05-12', 
                   '2023-06-01', '2023-06-20', '2023-07-05', '2023-07-10', '2023-07-15']
}
df_vendas = pd.DataFrame(dados_vendas_v3)
df_vendas['data_venda'] = pd.to_datetime(df_vendas['data_venda'])


# %%
# 1 Descubra quais são os 3 produtos que representam o maior lucro bruto potencial total em estoque. 
df_1 = df_estoque.copy()
df_1['preco_bruto'] = df_1['preco_venda'] - df_1['custo_fornecedor'] 
df_1['lucro_potencial'] = df_1['preco_bruto'] * df_1['estoque']
lucro_potencial = df_1.nlargest(3, 'lucro_potencial')[['modelo', 'lucro_potencial']].reset_index(drop=True)
lucro_potencial


# %%
# 2 Precisamos enviar um brinde para o cliente que mais deixou dinheiro na loja. Descubra qual 
# cliente teve o maior gasto acumulado em todo o histórico. Imprima o nome do cliente e o total gasto. 
df_1 = df_estoque.merge(right=df_vendas, how='inner', on='modelo')
df_1['gastos'] = df_1['preco_venda'] * df_1['quantidade']
top_cliente = df_1.groupby('cliente')['gastos'].sum().sort_values(ascending=False).head(1)
nome_cliente = top_cliente.index[0]
gasto_cliente = top_cliente.values[0]
print(f'nome: {nome_cliente}, gasto: {gasto_cliente}')

# %%
# 3 O custo das coisas subiu. Aplique um aumento de 10% no preco_venda de todos os produtos da categoria
#  "Periféricos", mas Apenas naqueles em que o lucro bruto unitário atual (preço - custo) seja menor que R$ 150,00.
df_3 = df_estoque.copy()
df_3['lucro_bruto'] = df_3['preco_venda'] - df_3['custo_fornecedor']
linhas_alvo = (df_3['categoria'] == 'Periféricos') & (df_3['lucro_bruto'] < 150)
df_3.loc[linhas_alvo, 'preco_venda'] = df_3.loc[linhas_alvo, 'preco_venda'] * 1.10
df_3
# %%
