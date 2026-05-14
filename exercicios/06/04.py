# %%
# 06.04 Quem teve mais transacoes de Streak?

import pandas as pd

# %%
transacoes  = pd.read_csv('../../data/transacoes.csv', sep=';')
transacoes.head()

# %%
transacao_produto = pd.read_csv("../../data/transacao_produto.csv", sep=';')
transacao_produto.head()

# %%
produtos = pd.read_csv("../../data/produtos.csv", sep=';')
produtos.head()



# %%
clientes_transacao_produto = transacoes.merge(transacao_produto, on='Idtransacao', how='left')[['idTransacao', "idCliente", "idProduto"]]

df_full = clientes_transacao_produto.merge(produtos, on=['IdProduto'], how='left')

df_full = df_full[df_full['DescProduto'] == 'Presenca Streak']

(df_full.groupby(by=['IdCliente'])['IdTransacao']
        .count()
        .sort_values(ascending=False)
        .head(1)
)



# %%
# jeito mais pratico, porem dificil
produtos = produtos[produtos["descProduto"]=="Presença Streak"]

(transacoes.merge(transacao_produto, on=["idTransacao"], how="left")
           .merge(produtos, on=["idProduto"], how="inner")
           .groupby(by="idCliente")["idTransacao"]
           .count()
           .sort_values(ascending=False)
           .head(1)
)