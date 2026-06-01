# %% 
import pandas as pd

# %% 
df_clientes = pd.read_csv('../../data/clientes.csv', sep=';')
df_produtos = pd.read_csv('../../data/produtos.csv', sep=';')
df_transacoes = pd.read_csv('../../data/transacoes.csv', sep=';')
df_transacao_produto = pd.read_csv('../../data/transacao_produto.csv', sep=';')



# %%
# 1 Calcule e exiba a média, a mediana e o valor máximo da coluna qtdePontos da tabela de clientes
media = df_clientes['qtdePontos'].mean()
mediana = df_clientes['qtdePontos'].median()
maximo = df_clientes['qtdePontos'].max()

print(f"Média de pontos: {media:.2f}")
print(f"Mediana de pontos: {mediana:.2f}")
print(f"Valor máximo: {maximo}")



# %%
# 2 Usando a DtCriacao da tabela de clientes, descubra qual foi o par "Ano-Mês" (ex: 2024-02) que registrou a maior quantidade de contas criadas.
df_clientes['DtCriacao'] = pd.to_datetime(df_clientes['DtCriacao'])
df_clientes['ano_mes'] = df_clientes['DtCriacao'].dt.to_period('M')
ranking_periodos = df_clientes['ano_mes'].value_counts()

periodo_pico = ranking_periodos.index[0]
quantidade_pico = ranking_periodos.iloc[0]

print(f"O pico de cadastros foi em {periodo_pico} com {quantidade_pico} novas contas.")
# %%
