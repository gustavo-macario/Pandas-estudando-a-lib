# %%

import pandas as pd

dados = {
    "id_funcionario": ["FUNC-101", "FUNC-102", "FUNC-103", "FUNC-104", "FUNC-105"],
    "nome_completo": ["ana silva", "carlos dias", "marta souza", "joão pedro", "lucas alves"],
    "departamento": ["Vendas", "TI", "RH", "TI", "Vendas"],
    "salario_mensal": ["R$ 2.500,50", "R$ 6.800,00", "R$ 4.200,75", "R$ 8.100,00", "R$ 3.100,20"],
    "tempo_empresa": ["2 anos", "5 anos", "3 anos", "10 anos", "1 ano"],
    "nota_avaliacao": ["8,5", "9,0", "7,2", "9,5", "6,8"],
    "faltas_no_ano": [2, 0, 1, 0, 4]
}

df_func = pd.DataFrame(dados)
df_func



# %%
# Extrair ID: Crie uma função que receba a string de id_funcionario (ex: "FUNC-101") 
# e retorne apenas o número (ex: "101"). Aplique essa função para atualizar a coluna.
def id_int(id):
    return int(id.replace("FUNC-", ""))

df_func['id_funcionario'].apply(id_int)
      


# %%
# Formatar Nome: Use o apply para transformar os nomes da coluna nome_completo para letra maiúscula.
def to_upper(n):
    return n.title().upper()

df_func['nome_completo'].apply(to_upper)



# %%
# Limpar Salário: Crie uma função para converter o salario_mensal de string para float. 
# Lembre-se de remover o "R$ ", tirar os pontos de milhar (".") e trocar a vírgula (",") por ponto (".").
def str_to_float(s):
    return float(s.replace("R$", "")
                 .replace(" ", "")
                 .replace(",", ""))

df_func['salario_mensal'].apply(str_to_float)



# %%
# Limpar Tempo de Empresa: Crie uma função para remover a palavra " anos" ou " ano" da coluna tempo_empresa 
# e converter o resultado para número inteiro (int).
def remove_ano(a):
    return int(a.replace(" ", "")
               .replace("anos", "")
               .replace("ano", ""))

df_func['tempo_empresa'] = df_func['tempo_empresa'].apply(remove_ano)



# %%
# Converter Nota: Transforme a coluna nota_avaliacao de string para float, substituindo a vírgula por ponto.
def nota_to_float(n):
    return float(n.replace(",", "."))

df_func['nota_avaliacao'].apply(nota_to_float)



# %%
# Classificar Nível: Crie uma função que receba o tempo de empresa (já numérico) e retorne "Júnior" se for 
# até 2 anos, "Pleno" se for de 3 a 5 anos, e "Sênior" se for maior que 5. Crie uma nova coluna chamada
# nivel_cargo usando .apply().
def cargos(a):
    if a <= 2:
        return 'Junior'
    elif a <= 5:
        return 'Pleno'
    else:
        return 'Sênior'
    
df_func['nivel_cargo'] = df_func['tempo_empresa'].apply(cargos)
    


# %%
# Mapear Setor: Crie uma função que classifique o departamento em "Operacional" (se for Vendas) ou 
# "Estratégico/Suporte" (se for TI ou RH). Crie a coluna tipo_setor.
def cla_dep(d):
    if d == 'Vendas':
        return "Operacional"
    elif d in ['TI', 'RH']:
        return "Estratégico/Suporte"
    
df_func['tipo_setor'] = df_func['departamento'].apply(cla_dep)
df_func



# %%
# Bônus de Desempenho: Crie uma função que receba a linha inteira. Se a nota_avaliacao for maior ou igual 
# a 8.5 E as faltas_no_ano forem iguais a 0, a função deve retornar True (elegível para bônus), caso contrário,
# False. Crie a coluna elegivel_bonus usando .apply(..., axis=1).
def bonus(linha):
    if linha['nota_avaliacao'] >= 8.5 and linha['faltas_no_ano'] == 0:
        return True
    else:
        return False
    
df_func['elegivel_bonus'] = df_func.apply(bonus, axis=1)



# %%
# Ajuste Salarial: Crie uma função de linha que calcule o novo salário. Se o funcionário for de "TI", 
# aplique um aumento de 10% no salario_mensal. Se for de outro setor, aplique 5%. Substitua os valores na 
# coluna salario_mensal.
df_func['salario_mensal'] = df_func['salario_mensal'].apply(str_to_float)
def novo_sal(linha):
    if linha['departamento'] == 'TI':
       return linha['salario_mensal'] * 1.10
    else:
        return linha['salario_mensal'] * 1.05

df_func['salario_mensal'] = df_func.apply(novo_sal, axis=1)



# %%
# Resumo do Perfil: Crie uma função de linha que junte informações em uma frase. A função deve retornar
# uma string no formato: "[Nome] trabalha no setor de [Departamento] e tem nota [Nota].". 
# Salve o resultado na coluna resumo_perfil.
def infos(linha):
    return f"{linha['nome_completo']} trabalha no setor de {linha['departamento']} e tem nota {linha['nota_avaliacao']}"

df_func['resumo_perfil'] = df_func.apply(infos, axis=1)

# %%
