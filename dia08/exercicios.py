# %%
import pandas as pd

# Tabela de Clientes
df_clientes = pd.DataFrame({
    "idCliente": [1, 2, 3, 4, 5, 6],
    "nome": ["Ana", "Bruno", "Carlos", "Diana", "Eduardo", "Fernanda"],
    "estado": ["SP", "RJ", "MG", "SP", "BA", "RS"],
    "status": ["Ativo", "Ativo", "Inativo", "Ativo", "Ativo", "Inativo"]
})

# Tabela de Pedidos
df_pedidos = pd.DataFrame({
    "idPedido": [101, 102, 103, 104, 105, 106, 107, 108],
    "id_do_cliente": [1, 1, 2, 99, 4, 1, 5, 88], # Atenção aos IDs 99 e 88
    "data": ["01/05", "02/05", "02/05", "03/05", "04/05", "05/05", "05/05", "06/05"],
    "status": ["Enviado", "Processando", "Enviado", "Cancelado", "Enviado", "Enviado", "Processando", "Enviado"] 
})

# Tabela de Produtos
df_produtos = pd.DataFrame({
    "codProduto": [10, 20, 30, 40, 50, 60],
    "nome": ["Teclado", "Mouse", "Monitor", "Cadeira", "Headset", "Webcam"], 
    "preco": [150.0, 50.0, 800.0, 500.0, 200.0, 350.0]
})

# Tabela de Itens (O detalhe do que tem dentro de cada pedido)
df_itens_pedido = pd.DataFrame({
    "idPedido": [101, 101, 102, 103, 104, 105, 107, 109], # Atenção ao pedido 109
    "codProduto": [10, 20, 30, 20, 40, 50, 10, 99], # Atenção ao produto 99
    "quantidade": [1, 1, 1, 2, 1, 1, 3, 1]
})


# %%
# 1 Faça um merge entre df_pedidos e df_clientes para trazer apenas os pedidos que possuem um cliente válido correspondente na base de clientes. 
# Atente-se aos nomes das chaves de ligação.
df_pedidos.merge(df_clientes, left_on=['id_do_cliente'], right_on=['idCliente'], how='inner')



# %%
# 2 Foco no Cliente (Left Join): Precisamos de um relatório de todos os clientes cadastrados, 
# independentemente de terem feito pedidos ou não. Cruze df_clientes (esquerda) com df_pedidos (direita).
df_clientes.merge(df_pedidos, left_on=['idCliente'], right_on=['id_do_cliente'], how='left')



# %%
# 3 Conflito de Nomes (Suffixes): Note que tanto df_clientes quanto df_pedidos possuem uma coluna 
# chamada status. Faça o mesmo merge do exercício 1, mas use o parâmetro suffixes para renomear essas 
# colunas automaticamente para _Cliente e _Pedido.
df_pedidos.merge(df_clientes, left_on=['id_do_cliente'], right_on=['idCliente'], how='inner', suffixes=['_Pedido', '_Cliente'])



# %%
# 4 O Lado Direito da Força (Right Join): Cruze df_itens_pedido (esquerda) com df_produtos (direita) usando 
# how='right'. O objetivo é garantir que todos os produtos do nosso catálogo apareçam no resultado final, 
# mesmo que a quantidade vendida seja nula (Nulo/NaN).
df_itens_pedido.merge(right=df_produtos, how='right', on='codProduto')



# %%
# 5 O Retrato Completo (Outer Join): Faça uma junção total (how='outer') entre df_clientes e df_pedidos.
#  Observe o DataFrame resultante: você deve ver tanto os clientes que não compraram nada, quanto os pedidos
#  "fantasmas" (cujos IDs de cliente não existem no cadastro).
df_clientes.merge(df_pedidos, left_on=['idCliente'], right_on=['id_do_cliente'], how='outer')



# %%
# 6 Investigação de Órfãos: Aproveitando a lógica de left join do exercício 2, escreva um código que junte as tabelas 
# e depois use um filtro do pandas (como o .isna()) para retornar um DataFrame apenas com os clientes que nunca 
# fizeram um pedido.
df_left= df_clientes.merge(df_pedidos, left_on=['idCliente'], right_on=['id_do_cliente'], how='left')
clientes_sem_pedido = df_left[df_left['idPedido'].isna()]
clientes_sem_pedido


# %%
# 7 Merge em Cadeia: Queremos saber o detalhe financeiro dos pedidos. Primeiro, faça um merge de df_itens_pedido
# com df_produtos. Em seguida, crie uma nova coluna no DataFrame resultante chamada valor_total_item, multiplicando 
# a quantidade pelo preço.
df_total = df_itens_pedido.merge(right=df_produtos,  how='inner', on='codProduto')
df_total['valor_total_item'] = df_total['quantidade'] * df_total['preco']
df_total



# %%
# 8 Apenas as Colunas Necessárias: É uma boa prática não arrastar colunas inúteis. Faça um merge entre df_pedidos e o
# df_clientes, mas traga do DataFrame de clientes apenas as colunas idCliente, nome e estado.
clientes = df_clientes[['idCliente', 'nome', 'estado']]
df_pedidos.merge(clientes, left_on=['id_do_cliente'], right_on=['idCliente'], how='inner')[['idCliente', 'nome', 'estado']]



# %%
# 9 O Investigador Silencioso (Dica de Parâmetro): Refaça o exercício 5 (Outer join entre clientes e pedidos),
# mas adicione o parâmetro indicator=True dentro da função merge(). Rode o código e olhe para a última coluna da 
# direita. Isso é extremamente útil em auditorias de dados.
df_clientes.merge(df_pedidos, left_on=['idCliente'], right_on=['id_do_cliente'], how='outer', indicator=True)



# %%
# 10 Junte as quatro tabelas passo a passo (df_clientes -> df_pedidos -> df_itens_pedido -> df_produtos). 
# Lide com os sufixos da coluna nome (que existe no cliente e no produto) e da coluna status. Ao final, 
# retorne um DataFrame que responda visualmente à pergunta: "Quais os nomes dos clientes que compraram um Monitor, 
# e qual o estado (UF) deles?"
df1 = df_clientes.merge(df_pedidos, left_on=['idCliente'], right_on=['id_do_cliente'], how='inner', suffixes=['_Cliente', '_Pedido'])
df2 = df1.merge(right=df_itens_pedido, how='inner', on='idPedido')
df3 = df2.merge(right=df_produtos, how='inner', on='codProduto', suffixes=['_Cliente', '_Produto'])
resultado_final = df3[df3['nome_Produto'] == 'Monitor' ][['nome_Cliente', 'estado']]
resultado_final



# %%
# 11 Crie um DataFrame que mostre o nome do cliente e a soma total do valor gasto por ele.
total_c = df3
total_c['total'] = total_c['quantidade'] * total_c['preco']
faturamento_cliente = total_c.groupby(by='idCliente')['total'].sum().reset_index()
faturamento_cliente



# %%
# 12 Aproveitando o resultado do exercício 11, a equipe de Marketing quer enviar um brinde 
# apenas para os clientes que gastaram mais de R$ 600,00 no total.
# Filtre o DataFrame gerado no exercício anterior para exibir apenas esses clientes VIP.
clientes_vip = faturamento_cliente[faturamento_cliente['total'] > 600] 
clientes_vip



# %%
# 13 junte df_clientes e df_pedidos (trazendo apenas pedidos válidos) e conte quantos pedidos existem para cada estado.
qtde_p = df_clientes.merge(df_pedidos, left_on=['idCliente'], right_on=['id_do_cliente'], how='inner', suffixes=['_Cliente', '_Pedido'])
qtde_p = qtde_p.groupby(by='estado')['idPedido'].count().reset_index()
qtde_p



# %%
# 14 Junte df_produtos e df_itens_pedido. Use a lógica do .isna() que você dominou no exercício 6 para descobrir qual é o nome 
# desse produto esquecido no estoque.
p_esquecido = df_produtos.merge(df_itens_pedido, how='left', on='codProduto')
p_esquecido = p_esquecido[p_esquecido['idPedido'].isna()]
p_esquecido



# %%
# 15 Junte df_produtos e df_itens_pedido. Agrupe pelo nome do produto e some a coluna quantidade. Por fim, ordene o resultado 
# para descobrir qual produto está no topo da lista.
p_top = df_produtos.merge(df_itens_pedido, how='inner', on='codProduto')
p_top = p_top.groupby(by='nome')['quantidade'].sum().reset_index()
p_top = p_top.sort_values(by='quantidade', ascending=False)
p_top



# %%
# 16 criar um DataFrame que contenha:
# O nome do Estado.
# A soma total de Valor vendida naquele estado.
# A Quantidade total de pedidos feitos naquele estado.
# Uma coluna calculada chamada ticket_medio (Soma Valor / Quantidade de Pedidos).
estado = df_clientes.merge(df_pedidos, left_on='idCliente', right_on='id_do_cliente', how='inner')
estado
estado = estado.merge(df_itens_pedido, how='inner', on='idPedido')
estado = estado.merge(df_produtos, how='inner', on='codProduto')
estado['total'] = estado['quantidade'] * estado['preco']
resumo_estado = estado.groupby('estado').agg({
    'total': 'sum',
    'idPedido': 'nunique' 
}).reset_index()
resumo_estado['ticket_medio'] = resumo_estado['total'] / resumo_estado['idPedido']
resumo_estado
# %%
