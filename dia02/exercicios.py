# 1- Leitura e Separadores: Carregue o arquivo ../data/produtos.csv em uma variável chamada df_produtos. 

# %%
import pandas as pd

df_produtos = pd.read_csv("data/produtos.csv", sep=";")


# %%

# 2- Espionando o Início: Exiba as 7 primeiras linhas do DataFrame para entender a cara dos seus dados.
print(df_produtos.head(n=7))



# 3- Sorteio: Exiba uma amostra aleatória de 12 produtos diferentes.
print(df_produtos.sample(n=12))



# 4- Raio-X do DataFrame: Descubra exatamente quantas linhas e colunas existem na tabela, e depois verifique quais são os tipos de dados (dtypes) de cada coluna.
print(df_produtos.shape)
print(df_produtos.dtypes)


# 5- Renomeação Estratégica: Crie um dicionário para renomear pelo menos duas colunas. Por exemplo, mude descProduto para descricao e vlrPreco para preco. Aplique essa mudança no DataFrame.
new_products = {
    "DescNomeProduto": "DescNomeP",
    "DescDescricaoProduto": "DescDescricaoP"
}

df_produtos = df_produtos.rename(columns = new_products)



# 6- Seleção Específica (O "SELECT" do Pandas): Crie um novo DataFrame (ou reatribua o atual) que contenha apenas 3 colunas: o ID do produto, a descrição e o nome.
new_df_produtos = df_produtos[['IdProduto', 'DescDescricaoP', 'DescNomeP']]
print(new_df_produtos)



# 7- Espionando o Fim: Exiba as 5 últimas linhas desse novo DataFrame filtrado.
print(new_df_produtos.tail(5))



# 8- Organização Alfabética: Pegue a lista de colunas atual do seu DataFrame, ordene-a em ordem alfabética e reatribua essa ordem ao DataFrame, para que as colunas
#  mudem de posição.
df_produtos_sort = list(df_produtos)
df_produtos_sort.sort()
df_produtos = df_produtos[df_produtos_sort]
print(df_produtos)


# 9- Exportação Moderna: Salve esse DataFrame organizado e filtrado no formato Parquet, com o nome produtos_limpos.parquet. Lembre-se de ignorar o índice.
new_df_produtos.to_parquet("produtos_limpos.parquet", index=False)



# 10- Prova Real: Leia o arquivo produtos_limpos.parquet que você acabou de criar em uma nova variável chamada df_verificacao, 
# e use o comando que mostra o uso de memória profundo para garantir que o arquivo foi lido perfeitamente.
df_verificacao = pd.read_parquet("produtos.parquet")
df_verificacao.info(memory_usage='deep')



# 11 - A coluna IdProduto possui valores no formato "001 - Espada Longa".
# Escreva o código para limpar essa coluna de forma que ela contenha apenas os números (ex: "001", "002"). Substitua a coluna original no DataFrame com esse resultado limpo.
df_produtos["IdProduto"] = df_produtos["IdProduto"].str.split(" - ", expand=True)[0]
print(df_produtos)



# 12- Você precisa encontrar equipamentos com propriedades de buff (melhoria de status).
# Escreva o código para filtrar e exibir o DataFrame mostrando apenas os produtos onde a coluna DescDescricaoP contenha a palavra "aumenta".
filtro_buff = df_produtos["DescDescricaoP"].str.contains("aumenta", case=False)
print(df_produtos[filtro_buff])



# 13- Para equilibrar o inventário do jogo, precisamos saber a distribuição dos itens.
# Escreva o comando exato que retorna quantos produtos existem de cada tipo dentro da coluna DescCategoriaProduto (quantas espadas, quantas armaduras, etc.).
print(df_produtos["DescCategoriaProduto"].value_counts())



# 14- O sistema precisa identificar rapidamente o que é equipamento mágico.
# Crie uma nova coluna no DataFrame chamada EhMagico. O valor dessa coluna deve ser True se a categoria (DescCategoriaProduto) for "cajado" OU "chapeu", e False para todas as outras categorias.
EhMagico = df_produtos["DescCategoriaProduto"].str.contains("cajado|chapeu", case=False)
print(EhMagico)



# 15- O time de interface (UI) precisa saber quais descrições podem estourar o layout da tela.
# Crie uma nova coluna temporária que calcule o número de caracteres de cada texto da coluna DescDescricaoProduto. 
# Em seguida, exiba apenas as colunas DescNomeProduto e DescCategoriaProduto dos 3 produtos que possuem as descrições mais longas.
df_produtos["TamanhoDesc"] = df_produtos["DescDescricaoP"].str.len()

resultado_ui = df_produtos.sort_values(by="TamanhoDesc", ascending=False).head(3)

print(resultado_ui[['DescNomeP', 'DescCategoriaProduto']])