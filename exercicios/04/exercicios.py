# %%
import pandas as pd

# %%
# 04.01 - Quantos clientes tem vínculo com a Twitch?

df = pd.read_csv('../../data/clientes.csv', sep=';')

filtro = df['flTwitch'] == 1

qtde_twitch = df[filtro].shape[0]

print(f'Tem um total de {qtde_twitch} clientes com vinculo na Twitch')




# %%
# 04.02 - Quantos clientes tem um saldo de pontos maior que 1000?

filtro2 = df['qtdePontos'] >= 1000
qtde_1000 = df[filtro2].shape[0]
print(f'Tem um total de {qtde_1000} clientes com um saldo maior que 1000.')



# %%
# 04.03 - Quantas transações ocorreram no dia 2025-02-01?
df_transacoes = pd.read_csv('../../data/clientes.csv', sep=';')
filtro3 = (df_transacoes['DtCriacao'] >= '2025-02-01') & (df_transacoes['DtCriacao'] < '2025-02-02')
qtde_02_01 = df_transacoes[filtro3].shape[0]
print(f"No dia 2025-02-01 tivemos {qtde_02_01} transacoes")
