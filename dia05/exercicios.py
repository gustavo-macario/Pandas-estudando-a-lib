# %%

import pandas as pd

# DataFrame com dados "sujos" de um sistema de RH
dados = {
    "id_func": [1, 2, 3, 3, 4, 4, 5, None],
    "nome": ["Ana", "Bruno", "Carlos", "Carlos", "Diana", "Diana", "Eduardo", None],
    "departamento": ["TI", "RH", "Vendas", "Vendas", "TI", "TI", None, None],
    "salario_str": ["4500.50", "3200.00", "5000.00", "5500.00", "7000.00", "7000.00", None, None],
    "idade": [28, 34, 45, 45, None, None, 40, None],
    "dt_admissao": ["2023-01-15", "0000-00-00", "2021-05-20", "2021-05-20", "2020-11-10", "2020-11-10", "2022-08-01", None]
}

df_rh = pd.DataFrame(dados)


# %%

# Questão 1 (Remoção de Linhas Fantasmas):
# Existe uma linha no sistema onde absolutamente todos os dados vieram vazios. Escreva o código que remova apenas as linhas onde todas as colunas sejam NaN. 
# Sobrescreva o df_rh com esse resultado.
df_rh = df_rh.dropna(how='all')
df_rh



# %%

# Questão 2 (Conversão de Tipo):
# A coluna salario_str veio do banco de dados como texto. Converta essa coluna para o tipo float e crie uma nova coluna chamada salario.
df_rh['salario'] = df_rh['salario_str'].astype(float)
df_rh



# %%
# Questão 3 (Correção e Conversão de Data):
# O funcionário Bruno teve um bug no sistema e sua data veio como "0000-00-00". 
# Usando dicionário e o método replace, troque esse valor por "2022-02-01". Na mesma linha de código (ou na de baixo), 
# converta a coluna dt_admissao para o formato de data (datetime). Sobrescreva a coluna original.
replace = {"0000-00-00": "2022-02-01"}

df_rh['dt_admissao'] = pd.to_datetime(df_rh['dt_admissao'].replace(replace))
df_rh



# %%
# Questão 4 (Extração de Data):
# O RH quer fazer uma festa para os aniversariantes de tempo de empresa. Usando a propriedade .dt, extraia apenas 
# o mês da coluna dt_admissao e guarde em uma nova coluna chamada mes_admissao.
df_rh['mes_admissao'] = df_rh['dt_admissao'].dt.month
df_rh



# %%
# Questão 5 (Preenchimento Estático):
# Alguns funcionários vieram sem o departamento preenchido. Use o método correto para preencher os valores nulos (NaN) 
# da coluna departamento com a string "Sem Setor". Sobrescreva a coluna.
df_rh['departamento'] = df_rh['departamento'].fillna('Sem Setor')
df_rh



# %%
# Questão 6 (Preenchimento Dinâmico com Média):
# A Diana não informou a idade. Para não prejudicar o modelo preditivo, preencha os valores NaN da coluna idade com a média de 
# idade do resto da empresa. Sobrescreva a coluna.
medias = df_rh['idade'].mean()
df_rh['idade'] = df_rh['idade'].fillna(medias)



# %%
# Questão 7 (Filtro Específico de Nulos):
# Ainda sobrou um problema: o Eduardo está sem salário cadastrado (ficou NaN). Não podemos manter funcionários sem salário na base.
# Remova as linhas que possuem NaN especificamente e obrigatoriamente na coluna salario.
df_rh = df_rh.dropna(subset=['salario'])



# %%
# Questão 8 (Remoção de Duplicatas Exatas):
# A funcionária Diana e todos os seus dados foram inseridos duas vezes de forma idêntica no sistema por um erro de clique.
# Remova duplicatas que sejam 100% idênticas, mantendo a primeira ocorrência. Sobrescreva o df_rh.
df_rh = df_rh.drop_duplicates()
df_rh



# %%
# Questão 9 (Atualização de Cadastro - Duplicata Parcial):
# O Carlos aparece duas vezes. Isso aconteceu porque ele teve um aumento de salário (de 5000 para 5500), gerando um novo registro,
# mas mantendo o mesmo id_func. Remova a duplicata do Carlos se baseando apenas na coluna id_func, mas garanta que o 
# registro que vai sobrar é o último (o que tem o salário atualizado). Sobrescreva o df_rh.
df_rh = df_rh.drop_duplicates(subset=["id_func"], keep="last")
df_rh



# %%
# Questão 10 (Encadeamento: O Maior Salário por Departamento):
# Gere um novo DataFrame chamado teto_departamento. Ele deve conter apenas um funcionário por departamento 
# (ou seja, você vai remover duplicatas usando a coluna departamento). Porém, a regra é clara: a pessoa que deve 
# representar o departamento é a que tem o maior salário.
teto_departamento = (df_rh.sort_values('salario', ascending = False)
                     .drop_duplicates(subset=['departamento'], keep='first')
                     )
teto_departamento

