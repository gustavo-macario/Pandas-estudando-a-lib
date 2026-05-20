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
# 1. Tempo de Vida do Cadastro
#Crie uma nova coluna no df_clientes chamada Dias_Desde_Atualizacao que calcule a diferença em dias entre a data de 
# hoje e a coluna DtAtualizacao.
df_clientes['DtAtualizacao'] = pd.to_datetime(df_clientes['DtAtualizacao'])
data_hoje = pd.Timestamp.now()
df_clientes['Dias_Desde_Atualizacao'] = (data_hoje - df_clientes['DtAtualizacao']).dt.days
df_clientes



# %%
# 2. Clientes "Fantasmas" (Left Anti-Join)
# Descubra se existe algum cliente na base df_clientes que nunca realizou nenhuma transação 
# (ou seja, não está no df_transacoes).
df_clientes.merge(right=df_transacoes, how='left', on=['IdCliente'])



# %%
# 3. Busca Textual por Palavras-Chave
# No df_produtos, filtre todos os produtos cuja DescDescricaoProduto contenha a palavra "mágico" ou "mágica".
# Garanta que o filtro não seja sensível a letras maiúsculas ou minúsculas (case-insensitive).
filtro = df_produtos['DescDescricaoProduto'].str.contains('mágico|mágica', case=False, na=False)
df_produtos_filtrados = df_produtos[filtro]
df_produtos_filtrados
# %%
