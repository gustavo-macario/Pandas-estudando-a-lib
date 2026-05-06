# %%

import pandas as pd
import numpy as np

dados = {
    "id_funcionario": [101, 102, 103, 104, 105, 106, 107],
    "nome": ["Alice", "Bruno", "Carla", "Daniel", "Elena", "Fábio", "Gisele"],
    "idade": [28, 35, 28, 42, 35, 25, 25],
    "salario": [3500, 5200, 3500, 7000, 5200, 3000, 3000],
    "vendas_sem1": [120, 200, 150, 90, 200, 110, 110],
    "vendas_sem2": [130, 180, 150, 100, 210, 110, 130],
    "bater_meta": [1, 1, 0, 0, 1, 0, 1] # 1 = Bateu a meta, 0 = Não bateu
}

df_prova = pd.DataFrame(dados)


# %%
# Questão 1 (Aquecimento - I/O):
# Imagine que os dados acima estivessem em um arquivo chamado funcionarios.csv, e o separador fosse uma tabulação (TAB).
# Escreva a linha de código que leria esse arquivo e a linha que exibiria apenas os 5 primeiros registros.

df_prova = pd.read_csv("funcionarios.csv", sep='\t')
df_prova.head()



# %%
# Questão 2 (Operação Vetorial com Escalar):
# A diretoria decidiu dar uma bonificação fixa. Crie uma nova coluna chamada salario_bonus que adicione 500 ao valor atual da coluna salario.
df_prova['salario_bonus'] = df_prova['salario'] + 500



# %%
# Questão 3 (Operação Vetorial entre Colunas):
# Para avaliar o ano completo, crie uma nova coluna chamada vendas_totais que seja a soma das colunas vendas_sem1 e vendas_sem2.
df_prova['vendas_totais'] = df_prova['vendas_sem1'] + df_prova['vendas_sem2']



# %%
# Questão 4 (Intersecção de Dados - Produto):
# Queremos isolar o volume de vendas totais apenas de quem bateu a meta. Crie uma coluna chamada vendas_meta_atingida que seja o resultado da multiplicação entre vendas_totais e bater_meta.
df_prova['vendas_meta_atingida'] = df_prova['vendas_totais'] * df_prova['bater_meta']



# %%
# Questão 5 (Estatística Descritiva):
# O RH pediu um resumo estatístico (média, desvio padrão, mínimo, máximo, quartis) exclusivo da coluna salario. Escreva o código que gera esse relatório.
df_prova['salario'].describe()



# %%
# Questão 6 (Transformação com NumPy):
# Devido à alta variância nas vendas do segundo semestre, crie uma coluna chamada log_vendas_sem2 aplicando o logaritmo natural (via NumPy) sobre a coluna vendas_sem2.
# Adicione 1 à equação para evitar problemas matemáticos caso houvesse o valor zero.
df_prova['log_vendas_sem2'] = np.log(df_prova['vendas_sem2'] + 1)



# %%
# Questão 7 (Filtro por Agregação):
# Quem foi o campeão ou campeã de vendas no 1º semestre? Escreva o código que filtre e retorne o DataFrame contendo apenas a(s) linha(s) do(s) funcionário(s) 
# que obteve(obtiveram) o valor máximo na coluna vendas_sem1.
max_vendas_sem1 = df_prova['vendas_sem1'].max()
filtro_campeao = df_prova['vendas_sem1'] == max_vendas_sem1
df_prova[filtro_campeao]



# %%
# Questão 8 (Encadeamento e Extração de Série):
# Precisamos criar um comitê com os funcionários mais experientes (idade). Ordene os dados pela idade de forma decrescente (do mais velho para o mais novo), 
# pegue os 3 primeiros, e retorne apenas a coluna nome em formato de Série.
top_3_velhos = df_prova.sort_values(by="idade", ascending=False).head(3)['nome']




# %%
# Questão 9 (Ordenação Múltipla - Direção Única):
# O financeiro quer uma lista do mais caro ao mais barato. Ordene o DataFrame inteiro pelo salario e depois pelas vendas_totais. 
# O critério deve ser decrescente para ambos (maior salário no topo; em caso de empate, maiores vendas totais desempata).
top_maiores = df_prova.sort_values(by=['salario', 'vendas_totais'], ascending=False)



# %% 
# Questão 10 (Ordenação Múltipla - Direções Mistas):
# Ordene o DataFrame pelo salario do maior para o menor. 
# No entanto, se duas pessoas tiverem o mesmo salário, a pessoa mais nova deve ter prioridade e aparecer primeiro no desempate.
top_maiores2 = df_prova.sort_values(by=['salario', 'idade'], ascending=[False, True])