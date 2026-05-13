# %%
import pandas as pd

# %%
# 1Agrupe os dados por IdCliente e descubra quantas transações (IdTransacao) cada cliente realizou. Retorne uma Series.
df = pd.read_csv('../data/transacoes.csv', sep=';')

df.groupby(by=['IdCliente'])['IdTransacao'].count()



# %%
# 2Agrupe os dados por IdCliente e calcule a soma total de QtdePontos acumulada por cada cliente.
df.groupby(by=['IdCliente'])['QtdePontos'].sum()



# %%
# 3Faça a mesma contagem de transações do Exercício 1, mas garanta que o resultado seja um DataFrame e que a coluna IdCliente não se torne o índice.
df.groupby(by=['IdCliente'], as_index=False)['IdTransacao'].count()



# %%
# 4Agrupe os dados pela coluna DescSistemaOrigem e calcule a média, o valor máximo e o valor mínimo da coluna QtdePontos.
df.groupby(by=['DescSistemaOrigem']).agg({'QtdePontos': ['mean', 'max', 'min']})



# %%
# 5Crie um sumário onde você agrupa por IdCliente e, em uma única operação usando 
# .agg(), traga a contagem de IdTransacao e a soma de QtdePontos.
summary = df.groupby(by=['IdCliente']).agg({'IdTransacao' : ['count'],
                                            'QtdePontos': ['sum']})
summary



# %%
# 6Agrupe os dados por IdCliente e por DescSistemaOrigem. Em seguida, 
# conte quantas transações cada cliente fez em cada sistema.
df.groupby(by=['IdCliente', 'DescSistemaOrigem'])['IdTransacao'].count()



# %%
# 7Refaça o Exercício 5 e, em seguida, renomeie as colunas resultantes para acabar 
# com o MultiIndex. Os nomes finais devem ser: "IdCliente", "TotalTransacoes" e "SomaPontos".
summary = df.groupby(by=['IdCliente'], as_index=False).agg({
        'IdTransacao' : ['count'],
        'QtdePontos': ['sum']
    })
summary.columns = ['IdCliente', 'TotalTransacoes', 'SomaPontos']
summary



# %%
# 8Crie uma função customizada em Python chamada calc_amplitude que receba uma Series 
# e retorne a diferença entre o valor máximo e o mínimo. Use essa função dentro de
#  um .groupby() por IdCliente para calcular a amplitude de QtdePontos.
def calc_amplitude(s):
    return (s.max() - s.min())

df.groupby(by=['IdCliente']).agg({'QtdePontos' : [calc_amplitude]})



# %%
# 9Crie uma função customizada chamada tempo_de_vida que recebe uma Series de datas,
#  converte para datetime usando Pandas e retorna a diferença em dias entre a data 
# máxima e a data mínima. Aplique isso agrupando por IdCliente na coluna DtCriacao.
def tempo_de_vida(s):
    s = pd.to_datetime(s)
    return (s.max() - s.min()).days

df.groupby(by=['IdCliente']).agg({'DtCriacao' : [tempo_de_vida]})



# %%
# 10Junte tudo! Agrupe por IdCliente e traga usando o .agg():
# A quantidade de transações.
# A soma, média e a sua função customizada de amplitude para os pontos.
# O tempo de vida do cliente (sua função de datas) usando a data de criação.
# Não esqueça de renomear as colunas no final para deixar o DataFrame limpo.

summary2 = df.groupby(by=['IdCliente'], as_index=False).agg({'IdTransacao' : ['count'],
                                  'QtdePontos': ['sum', 'mean', calc_amplitude],
                                  'DtCriacao': [tempo_de_vida]})

summary2.columns = ['IdCliente',
                    'QtdeTransacoes',
                    'Soma', 'Media', 'Amplitude',
                    'TempoDe Vida']
summary2



# %%
# 11 Agrupe os dados por IdCliente (trazendo como um DataFrame com as_index=False) e calcule a
#  soma de QtdePontos. Em seguida, ordene esse resultado para descobrir quem são os 
# 5 clientes com as maiores pontuações totais.
soma = df.groupby(by=['IdCliente'], as_index=False)['QtdePontos'].sum()
soma.sort_values(by='QtdePontos', ascending=False).head(5)



# %%
# 12 Será que os clientes usam mais de um sistema? Agrupe por IdCliente e descubra quantos sistemas 
# diferentes (únicos) cada cliente utilizou na coluna DescSistemaOrigem.
df.groupby(by=['IdCliente'])['DescSistemaOrigem'].nunique()



# %%
# 13 Agrupe os dados por DescSistemaOrigem, calcule a média da QtdePontos (trazendo como DataFrame) e,
# logo em seguida, arredonde o resultado para 2 casas decimais.
df.groupby(by=['DescSistemaOrigem'], as_index=False)['QtdePontos'].mean().round(2)



# %%
# 14 Primeiro, agrupe por IdCliente e calcule a soma total de QtdePontos (lembre-se do as_index=False). 
# Salve isso em uma variável. Depois, filtre esse novo DataFrame para mostrar apenas os clientes que
# acumularam estritamente mais de 50 pontos no total.
soma_pontos = df.groupby(by=['IdCliente'], as_index=False)['QtdePontos'].sum()
soma_pontos = soma_pontos[soma_pontos['QtdePontos'] > 50]
soma_pontos



# %%
# 15 Crie um sumário por IdCliente usando o .agg() que mostre a primeira vez que o cliente interagiu
#  (data mínima) e a última vez que ele interagiu (data máxima) usando a coluna DtCriacao. Renomeie as 
# colunas no final para "IdCliente", "PrimeiraTransacao" e "UltimaTransacao".
summary3 = df.groupby(by=['IdCliente'], as_index=False).agg({'DtCriacao': ['min', 'max']})
summary3.columns = ['IdCliente',
                    'PrimeiraTransacao',
                    'UltimaTransacao']
summary3
# %%
