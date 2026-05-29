# %% 
import pandas as pd

# %% 
df_clientes = pd.read_csv('../../data/clientes.csv', sep=';')
df_produtos = pd.read_csv('../../data/produtos.csv', sep=';')
df_transacoes = pd.read_csv('../../data/transacoes.csv', sep=';')
df_transacao_produto = pd.read_csv('../../data/transacao_produto.csv', sep=';')



# %%
# 1 Crie uma função em Python chamada resumo_tabelas que receba um número variável de DataFrames (args) e retorne um dicionário Python. As chaves do dicionário 
# devem ser o formato de cada tabela (ex: "tabela_1") e os valores devem ser tuplas contendo a quantidade de linhas e colunas correspondentes. Teste a função 
# com as quatro tabelas.
def resumo_tabelas(*args):
    dic = {}
    contador = 1
    for tabelas in args:
        nome_da_chave = f"tabela_{contador}"
        dic[nome_da_chave] = tabelas.shape
        contador += 1
    return dic
    
print(resumo_tabelas(df_transacao_produto, df_produtos))



# %%
# 2 Usando o df_produtos, filtre usando o pandas todos os produtos cuja DescCategoriaProduto seja "cajado". Em seguida, extraia os nomes 
# desses produtos (DescNomeProduto) e use uma list comprehension do Python nativo para criar uma nova lista com esses nomes convertidos 
# para letras maiúsculas.
lista_produtos = ()
df_2 = df_produtos.copy()
df_2 = df_2[df_2['DescCategoriaProduto'] == 'cajado']
nome_produtos = df_2['DescNomeProduto']
lista_produtos = nome_produtos.to_list()
lista_produtos_maiusculos = [p.upper() for p in lista_produtos]
lista_produtos_maiusculos



# %%
# 3 No df_clientes, temos várias colunas de flags para redes sociais (flTwitch, flYouTube, etc.). Crie uma nova coluna no DataFrame chamada 
# TotalRedesSociais que some essas flags (1 ou 0) para cada cliente. Utilize o método .apply() do Pandas em conjunto com uma função lambda 
# nativa do Python para realizar essa soma por linha.
df_clientes['TotalRedesSociais'] = df_clientes.apply(lambda linha: linha['flTwitch'] + linha['flYouTube'] + linha['flBlueSky'] + linha['flInstagram'] , axis=1)
df_clientes



# %%
# 4 Faça um merge entre df_transacao_produto e df_produtos usando a chave em comum (IdProduto). Crie uma nova coluna nessa tabela unificada
# chamada ReceitaTotal, que será o resultado da multiplicação da quantidade de produtos (QtdeProduto) pelo valor do produto (vlProduto).
df_4 = df_transacao_produto.merge(right=df_produtos, how='inner', on='IdProduto')
df_4['ReceitaTotal'] = df_4['QtdeProduto'] * df_4['vlProduto']
df_4



# %%
# 5 Com o DataFrame resultante da Questão 4, agrupe os dados por DescCategoriaProduto. Calcule a soma total da ReceitaTotal para cada categoria
# Além disso, crie uma agregação que retorne, em uma única string separada por vírgulas, todos os nomes de produtos únicos 
# (DescNomeProduto) vendidos dentro de cada categoria.
df_5 = df_4.groupby('DescCategoriaProduto').agg({
    'ReceitaTotal': 'sum',                     
    'DescNomeProduto': lambda x: ", ".join(x.unique())               
}).reset_index()
df_5



# %%
# 6 Na tabela df_transacoes, a coluna DtCriacao é uma string (texto). Converta essa coluna para o tipo datetime do pandas. 
# Depois, crie duas novas colunas: Ano e Mes. Crie um loop for do Python que itere sobre os meses únicos encontrados para imprimir
#  uma mensagem no console: "No mês X, tivemos Y transações."
df_transacoes['DtCriacao'] = pd.to_datetime(df_transacoes['DtCriacao'])
df_transacoes['Ano'] = df_transacoes['DtCriacao'].dt.year
df_transacoes['Mes'] = df_transacoes['DtCriacao'].dt.month
for mes in df_transacoes['Mes'].unique():
    quantidade = df_transacoes[df_transacoes['Mes'] == mes].shape[0]
    print(f"No mês {mes}, tivemos {quantidade} transações.")




# %%
# 7 Precisamos saber os sistemas de origem (DescSistemaOrigem) preferidos de clientes que compram "Armaduras". Faça uma sequência de merges
# conectando: df_produtos -> df_transacao_produto -> df_transacoes. Filtre apenas a categoria "armadura" e exiba qual foi o sistema 
# de origem com mais vendas (em quantidade) para essa categoria.
df_7 = df_produtos.merge(right=df_transacao_produto, how='inner', on='IdProduto')
df_7 = df_7.merge(right=df_transacoes, how='inner', on='IdTransacao')
df_7 = df_7[df_7['DescCategoriaProduto'] == 'armadura']
maior_sistema = df_7.groupby('DescSistemaOrigem')['IdTransacao'].count()
sistema_campeao = maior_sistema.sort_values(ascending=False).index[0]
print(f"O sistema de origem com mais vendas de armaduras foi: {sistema_campeao}")



# %%
# 8 Imagine que os dados da Twitch foram exportados separadamente. Filtre df_transacoes criando dois novos DataFrames: df_twitch 
# (onde o sistema de origem é 'twitch') e df_outros (qualquer outro sistema). Em seguida, embaralhe as linhas do df_twitch 
#. Por fim, utilize o pd.concat() para unir essas duas tabelas novamente e redefina o índice.
df_twitch = df_transacoes.copy()
df_twitch = df_twitch[df_twitch['DescSistemaOrigem'] == 'twitch']
df_outros = df_transacoes.copy()
df_outros = df_outros[df_outros['DescSistemaOrigem'] != 'twitch']

df_twitch = df_twitch.sample(frac=1)

df_final = pd.concat([df_twitch, df_outros], ignore_index=True)
df_final



# %%
# 9 Alguns clientes possuem uma quantidade de pontos muito alta (qtdePontos em df_clientes). Crie uma função Python normal chamada 
# classifica_cliente(pontos) que utilize blocos try/except (apenas para garantir que dados nulos ou textos acidentais não quebrem 
# o código, retornando "Desconhecido"). A função deve retornar "VIP" se pontos > 5000, "Regular" se entre 1000 e 5000, e "Iniciante" 
# se menor que 1000. Aplique essa função no DataFrame.
df_clientes

def classifica_cliente(pontos):
    try:
        if pontos < 1000:
            return 'Iniciante'
        elif pontos <= 5000:
            return 'Regular'
        else:
            return 'VIP'
    except:
        return 'Desconhecido'

df_clientes['Classificacao'] = df_clientes['qtdePontos'].apply(classifica_cliente)  
df_clientes



# %%
# 10 Qual cliente (exiba apenas o IdCliente) gerou a maior receita financeira comprando itens da categoria "espada"?
#  Requisitos: Você precisará fazer o join de todas as quatro tabelas, filtrar a categoria correta, realizar a operação matemática de
#  receita, agrupar pelo ID do cliente e encontrar o valor máximo usando métodos do Pandas.
df_10 = df_produtos.merge(right=df_transacao_produto, how='inner', on='IdProduto')
df_10 = df_10.merge(right=df_transacoes, how='inner', on='IdTransacao')
df_10 = df_10.merge(right=df_clientes, how='inner', on='IdCliente')
df_10 = df_10[df_10['DescCategoriaProduto'] == 'espada']
df_10['receita'] = df_10['QtdeProduto'] * df_10['vlProduto'] 
maior_cliente = df_10.groupby('IdCliente')['receita'].sum().idxmax()
maior_cliente
# %%
