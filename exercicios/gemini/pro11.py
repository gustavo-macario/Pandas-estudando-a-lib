# %%
import pandas as pd

estoque_hardware = {
    'item_1': {'categoria': 'Processador', 'modelo': 'Core i5 11400f', 'preco': 850.00, 'estoque': 15, 'score_desempenho': 75},
    'item_2': {'categoria': 'Placa de Vídeo', 'modelo': 'RTX 4060 8GB', 'preco': 1950.00, 'estoque': 8, 'score_desempenho': 88},
    'item_3': {'categoria': 'Placa Mãe', 'modelo': 'B560M', 'preco': 600.00, 'estoque': 20, 'score_desempenho': 50},
    'item_4': {'categoria': 'Processador', 'modelo': 'Ryzen 5 5600', 'preco': 900.00, 'estoque': 12, 'score_desempenho': 78},
    'item_5': {'categoria': 'Placa de Vídeo', 'modelo': 'RX 7600 8GB', 'preco': 1800.00, 'estoque': 5, 'score_desempenho': 85},
    'item_6': {'categoria': 'Memória RAM', 'modelo': '16GB DDR4 3200MHz', 'preco': 250.00, 'estoque': 30, 'score_desempenho': 60},
    'item_7': {'categoria': 'Fonte', 'modelo': '650W 80 Plus Bronze', 'preco': 400.00, 'estoque': 0, 'score_desempenho': 40},
    'item_8': {'categoria': 'Processador', 'modelo': 'Core i9 13900K', 'preco': 3800.00, 'estoque': 3, 'score_desempenho': 98},
    'item_9': {'categoria': 'Processador', 'modelo': 'Ryzen 7 5700X', 'preco': 1300.00, 'estoque': 10, 'score_desempenho': 85},
    'item_10': {'categoria': 'Placa de Vídeo', 'modelo': 'RTX 4090 24GB', 'preco': 12500.00, 'estoque': 2, 'score_desempenho': 100},
    'item_11': {'categoria': 'Placa de Vídeo', 'modelo': 'RTX 3060 12GB', 'preco': 1600.00, 'estoque': 15, 'score_desempenho': 78},
    'item_12': {'categoria': 'Armazenamento', 'modelo': 'SSD NVMe 1TB', 'preco': 450.00, 'estoque': 40, 'score_desempenho': 80},
    'item_13': {'categoria': 'Armazenamento', 'modelo': 'HD 2TB SATA', 'preco': 350.00, 'estoque': 18, 'score_desempenho': 35},
    'item_14': {'categoria': 'Placa Mãe', 'modelo': 'X670E', 'preco': 2200.00, 'estoque': 4, 'score_desempenho': 85},
    'item_15': {'categoria': 'Placa Mãe', 'modelo': 'A320M', 'preco': 350.00, 'estoque': 25, 'score_desempenho': 30},
    'item_16': {'categoria': 'Memória RAM', 'modelo': '32GB DDR5 6000MHz', 'preco': 850.00, 'estoque': 10, 'score_desempenho': 90},
    'item_17': {'categoria': 'Memória RAM', 'modelo': '8GB DDR4 2666MHz', 'preco': 130.00, 'estoque': 50, 'score_desempenho': 40},
    'item_18': {'categoria': 'Fonte', 'modelo': '850W 80 Plus Gold', 'preco': 800.00, 'estoque': 7, 'score_desempenho': 85},
    'item_19': {'categoria': 'Gabinete', 'modelo': 'Mid Tower RGB', 'preco': 350.00, 'estoque': 14, 'score_desempenho': 50},
    'item_20': {'categoria': 'Gabinete', 'modelo': 'Full Tower Premium', 'preco': 900.00, 'estoque': 0, 'score_desempenho': 80},
}


# %%
# 1 Transforme o dicionário estoque_hardware em um DataFrame do Pandas chamado df_loja.
# Dica leve: Se você jogar o dicionário direto no pd.DataFrame(), as chaves ('item_1') vão virar colunas. Pesquise sobre o 
# argumento orient='index' para que as chaves virem os índices das linhas.
df_estoque_hardware = pd.DataFrame.from_dict(estoque_hardware, orient='index')
df_estoque_hardware


# %%
# 2 Antes de fazer qualquer análise, imagine que o sistema tentou atualizar o preço do 'item_99' (que não existe no dicionário). 
# Crie um bloco try/except no Python puro que tente acessar e alterar o preço do estoque_hardware['item_99'] para 1000. Se a chave não existir, 
# o except deve imprimir "Erro: Peça não encontrada no sistema", sem quebrar o código.
def alterarPreco(dicionario, item_chave):
    try:
        dicionario[item_chave]['preco'] = 1000
        print("Preço alterado com sucesso!")
 
    except KeyError:
         print('produto nao encontrado')
    
alterarPreco(estoque_hardware, 'item_9')



# %%
# 3 Crie uma função em Python chamada classificar_peca(valor) que recebe um número (o preço). 
# Se o preço for maior que 1500, retorne 'Premium'. Se for entre 500 e 1500, retorne 'Intermediário'.
#  Menor que 500, 'Entrada'. Em seguida, use o .apply() no seu DataFrame para criar uma nova coluna chamada Segmento usando essa função.
def classificar_peca(valor):
    if valor > 1500:
        return 'Premium'
    elif valor >= 500:
        return 'Intermediário'
    else:
        return 'Entrada'
    
df_estoque_hardware['segmento'] = df_estoque_hardware['preco'].apply(classificar_peca)
df_estoque_hardware



# %%
# 4 Um cliente quer saber apenas as informações do 'i5 11400f' e da 'RTX 4060'. Usando os recursos de filtro do Pandas
# (como o .isin()), crie um novo DataFrame que contenha apenas as linhas onde o modelo seja exatamente um desses dois.
modelos = 'i5 11400f|RTX 4060'
df_4 = df_estoque_hardware[df_estoque_hardware['modelo'].str.contains(modelos, case=False, na=False)]
df_4


# %%
# 5 Crie uma coluna chamada Valor_Parado. Ela deve ser o resultado da multiplicação da coluna preco pela coluna estoque. 
# Descubra, usando Pandas, qual é a peça (modelo) que tem o maior valor financeiro total imobilizado no estoque da loja.
df_estoque_hardware['Valor_Parado'] = df_estoque_hardware['preco'] * df_estoque_hardware['estoque']
df_estoque_hardware = df_estoque_hardware.sort_values(by ='Valor_Parado', ascending=False)
top_peca = df_estoque_hardware.head(1)
top_peca


# %%
# 6 Use o .groupby() para descobrir duas coisas por categoria (Processador, Placa de Vídeo, etc.):
# A soma total de peças em estoque.
# A média do score_desempenho.
resumo = df_estoque_hardware.groupby('categoria').agg(
    soma=('estoque', 'sum'),
    media=('score_desempenho', 'mean')
)
resumo


# %%
# 7 A loja decidiu fazer uma queima de estoque relâmpago. Use uma função anônima (lambda) dentro de um .apply() 
# para aplicar 10% de desconto em todos os valores da coluna preco. Salve o resultado em uma nova coluna chamada Preco_Promocional.
df_estoque_hardware['Preco_Promocional'] = df_estoque_hardware['preco'] * 0.90
df_estoque_hardware


# %%
# 8 Por um erro no sistema, a loja recebeu um lote novo, mas esqueceu de cadastrar o preço. 
# Adicione essa linha diretamente no DataFrame:
df_estoque_hardware.loc['item_8'] = {'categoria': 'Processador', 'modelo': 'Core i3', 'preco': pd.NA, 'estoque': 10, 'score_desempenho': 60, 'Segmento': 'Entrada'}
# Agora, use o método .fillna() do Pandas para preencher esse preço vazio com a média de preços especificamente da categoria Processador.

media_processadores = df_estoque_hardware[df_estoque_hardware['categoria'] == 'Processador']['preco'].mean().round(2)
df_estoque_hardware['preco'] = df_estoque_hardware['preco'].fillna(media_processadores)
df_estoque_hardware


# %%
# 9 O time de compras precisa de um relatório limpo. Filtre o DataFrame para mostrar apenas os itens que têm estoque 
# maior que zero e que possuem um score_desempenho acima de 65. Ordene o resultado do melhor score para o pior usando .sort_values().
filtro = df_estoque_hardware[(df_estoque_hardware['estoque'] > 0) & (df_estoque_hardware['score_desempenho'] > 65)]
filtro = filtro.sort_values(by='score_desempenho', ascending=False)
filtro


# %%
# 10 Você tem um orçamento rigoroso de R$ 3.000,00. Escreva uma lógica (pode misturar laços for do Python percorrendo os
#  DataFrames filtrados com lógica condicional) para montar um PC que contenha exatamente:

# 1 Processador
# 1 Placa de Vídeo
# 1 Placa Mãe

# A regra é: a combinação não pode ultrapassar os R$ 3.000,00 de custo total, e você deve encontrar a combinação que 
# entregue a maior soma de score_desempenho possível dentro desse limite. Ao final, o código deve exibir o nome das 3 peças 
# escolhidas e o custo total.
df_10 = df_estoque_hardware.copy()
df_10 = df_10[df_10['estoque'] > 0]
df_10 = df_10.sort_values(by='score_desempenho', ascending=False)

processadores = df_10[df_10['categoria'] == 'Processador']
gpus = df_10[df_10['categoria'] == 'Placa de Vídeo']
placas_mae = df_10[df_10['categoria'] == 'Placa Mãe']

maior_score_encontrado = 0
melhor_combinacao = {}

for idx_p, proc in processadores.iterrows():
    for idx_g, gpu in gpus.iterrows():
        for idx_m, mae in placas_mae.iterrows():
            preco_total = proc['preco'] + gpu['preco'] + mae['preco']
            score_total = proc['score_desempenho'] + gpu['score_desempenho'] + mae['score_desempenho']
            
            if preco_total <= 3000 and score_total > maior_score_encontrado:
               maior_score_encontrado = score_total

               melhor_combinacao = {
                'Processador': proc['modelo'],
                'Placa de Vídeo': gpu['modelo'],
                'Placa Mãe': mae['modelo'] 
                }

print(melhor_combinacao)

# %%
