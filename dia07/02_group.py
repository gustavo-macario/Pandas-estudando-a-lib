# %%
import pandas as pd

transacoes = pd.read_csv("../data/transacoes.csv", sep=';')
transacoes

# %%
# agrupa por clientes e retorna as infos de todas as colunas
transacoes.groupby(by=['IdCliente']).count()


# %%
# agrupa por clientes e retorna as infos somente de 'IdTransacao'. retorna uma serie
transacoes.groupby(by=['IdCliente'])['IdTransacao'].count()


# %%
# mesma coisa acima mas retorna um dataframe, o id do cliente fica como indice
transacoes.groupby(by=['IdCliente'])[['IdTransacao']].count()

# o id do cliente nao fica mais como indice se usar o 'as_index=False'
transacoes.groupby(by=['IdCliente'], as_index=False)[['IdTransacao']].count()



# %%
summary = transacoes.groupby(by=['IdCliente'], as_index=False).agg({'IdTransacao': ['count'],
                                                          'QtdePontos': ['sum', 'mean']})

summary



# %%
# para acessar multi index
summary[{'QtdePontos', 'mean'}]

# com '.columns' ele acaba com o multi index e definimos como queremos as colunas
summary.columns = ['IdCliente', 'QtdeTransacao', "TotalPontos", "AvgPontos"]
summary