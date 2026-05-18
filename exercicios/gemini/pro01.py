# %% 
import pandas as pd

# %% 
# 1. Importe os 4 arquivos CSV para DataFrames distintos (df_clientes, df_produtos, df_transacoes, df_transacao_produto).
#  Atenção ao delimitador usado nos arquivos.
df_clientes = pd.read_csv('../../data/clientes.csv', sep=';')
df_produtos = pd.read_csv('../../data/produtos.csv', sep=';')
df_transacoes = pd.read_csv('../../data/transacoes.csv', sep=';')
df_transacao_produto = pd.read_csv('../../data/transacao_produto.csv', sep=';')




# %%
# 2. Verifique os tipos de dados de cada DataFrame. Converta as colunas de data (DtCriacao, DtAtualizacao) para o tipo datetime no Pandas.
df_clientes.dtypes
df_clientes['DtCriacao'] = pd.to_datetime(df_clientes['DtCriacao'])
df_clientes['DtAtualizacao'] = pd.to_datetime(df_clientes['DtAtualizacao'])

df_transacoes.dtypes
df_transacoes['DtCriacao'] = pd.to_datetime(df_transacoes['DtCriacao'])



# %%
# 3. Crie uma nova coluna no df_transacao_produto chamada ValorTotalItem, que deve ser o resultado da multiplicação
#  entre QtdeProduto e vlProduto.
df_transacao_produto['ValorTotalItem'] = df_transacao_produto['QtdeProduto'] * df_transacao_produto['vlProduto']




# %%
# 4. Usando o método apply, crie uma coluna chamada TipoProduto_Simples no df_produtos que contenha apenas a primeira
#  palavra do DescNomeProduto (ex: de "Espada Longa" para "Espada").
def first(p):
    return p.split()[0]
df_produtos['TipoProduto_Simples'] = df_produtos['DescNomeProduto'].apply(first)
df_produtos



# %%
# 5. Filtre o df_clientes para encontrar apenas os usuários que têm conta conectada na Twitch e no YouTube.
filtro = (df_clientes['flTwitch'] == 1) & (df_clientes['flYouTube'] == 1)
df_clientes_filtrado = df_clientes[filtro]
df_clientes_filtrado



# %%
# 6. No df_transacoes, crie duas colunas novas: Ano_Transacao e Mes_Transacao, extraídas da coluna DtCriacao.
df_transacoes['Ano_Transacao'] = df_transacoes['DtCriacao'].dt.year
df_transacoes['Mes_Transacao'] = df_transacoes['DtCriacao'].dt.month
df_transacoes



# %%
# 7. Crie uma função e use o apply no df_clientes para classificar o nível de engajamento do cliente. Se ele tiver mais de 2 redes
#  sociais conectadas (soma das colunas fl... maior que 2), retorne "Alto", caso contrário, "Baixo".
def nivel(linha):
    total = linha['flTwitch'] + linha['flYouTube'] + linha['flBlueSky'] + linha['flInstagram']
    if total > 2:
        return 'Alto'
    else:
        return 'Baixo'
df_clientes['Nivel'] = df_clientes.apply(nivel, axis=1)
df_clientes



# %%
# 8. Faça um merge entre df_transacoes e df_clientes para trazer as informações do cliente para a tabela de transações. 
# Chame este DataFrame de df_vendas_clientes.
df_vendas_clientes = df_transacoes.merge(right=df_clientes, how='inner', on=['IdCliente'])
df_vendas_clientes



# %%
# 9. Faça outro merge unindo df_transacao_produto e df_produtos para saber qual produto específico foi vendido em cada linha. 
# Chame de df_itens_detalhados.
df_itens_detalhados = df_transacao_produto.merge(right=df_produtos, how='inner', on=['IdProduto'])
df_itens_detalhados



# %%
# 10. Agora, o grande desafio de cruzamento: Crie um "Master DataFrame" fazendo o merge do resultado da questão 8 com o resultado da 
# questão 9, usando a coluna IdTransacao como chave.
master_df = df_vendas_clientes.merge(right=df_itens_detalhados, how='inner', on=['IdTransacao'])
master_df



# %%
# 11. Utilizando o groupby no DataFrame mestre, descubra qual é o DescSistemaOrigem que gerou o maior volume total de QtdePontos 
# nas transações.
resultado = master_df.groupby('DescSistemaOrigem', as_index=False)['QtdePontos'].sum().sort_values(ascending=False)
resultado.head(1)



# %%
# 12. Agrupe os dados por DescCategoriaProduto e descubra qual categoria gerou a maior receita total 
# (usando a coluna ValorTotalItem que você criou na questão 3).
master_df.groupby('DescCategoriaProduto')['ValorTotalItem'].sum().sort_values(ascending=False)



# %%
# 13. Qual é o Top 5 de clientes (IdCliente) que mais gastaram dinheiro na loja?
master_df.groupby('IdCliente')['ValorTotalItem'].sum().sort_values(ascending=False)



# %%
# 14. Descubra qual é o produto (DescNomeProduto) mais vendido em termos de quantidade absoluta (QtdeProduto).
master_df.groupby('DescNomeProduto')['QtdeProduto'].sum().sort_values(ascending=False).head(1)



# %%
# 15. Crie um relatório consolidado em um único DataFrame que mostre por IdCliente:
# A quantidade total de transações feitas.
# O valor total gasto.
# A categoria de produto favorita do cliente (aquela em que ele comprou mais itens).
relatorio = master_df.groupby('IdCliente').agg({
    'IdTransacao': 'nunique', 
    'ValorTotalItem': 'sum'   
})
favorita = master_df.groupby('IdCliente')['DescCategoriaProduto'].apply(lambda x: x.mode().iloc[0])
relatorio['categoria_favorita'] = favorita
relatorio
# %%
