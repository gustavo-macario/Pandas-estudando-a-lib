import pandas as pd

# ## Exercício 1: A Mágica do Pandas (Vetorização)

lista_precos = [10, 20, 30]
series_precos = pd.Series(lista_precos)

# DESAFIO:
# 1. Tente somar 5 direto na 'lista_precos' fazendo: lista_precos + 5 (Vai dar erro!)
lista = []
for n in lista_precos:
    n += 5
    lista.append(n)
print(lista)

# 2. Agora some 5 na 'series_precos' fazendo: series_precos + 5
des2 = series_precos + 5 
print(des2)


# ## Exercício 2: O Nome vs. A Cadeira (iloc)
alunos = pd.Series(['Ana', 'Bia', 'Caio', 'Davi'], index=[10, 20, 30, 40])

# DESAFIO: 
# Como você faz para pegar o nome 'Caio'? 
# 1. Tente pegar pelo nome da linha (o número 30).
print(alunos[30])

# 2. Tente pegar pela posição física dele usando o .iloc.
print(alunos.iloc[2])


# ## Exercício 3: A Dança dos Índices (sort_values)
pontuacoes = pd.Series([85, 40, 99, 70], index=['rodada1', 'rodada2', 'rodada3', 'rodada4'])
pontuacoes_ordenadas = pontuacoes.sort_values()

# DESAFIO:
# 1. Imprima 'pontuacoes_ordenadas'. Veja como o 40 foi para o topo.
print(pontuacoes_ordenadas)

# 2. Qual comando você usa para pegar esse valor 40 sem saber em qual 'rodada' ele aconteceu?
print(pontuacoes_ordenadas.iloc[0])


# ## Exercício 4: O Mistério do Varal Desigual
df_teste = pd.DataFrame()

serie_curta = pd.Series(['A', 'B']) # Tem 2 itens
serie_longa = pd.Series([100, 200, 300, 400]) # Tem 4 itens

df_teste['letras'] = serie_curta
df_teste['numeros'] = serie_longa

# DESAFIO:
# Imprima o df_teste. O que o Pandas colocou nas linhas da coluna 'letras' onde estava faltando informação?
print(df_teste)
# Retornou NaN, porque para o df precisa ter o mesmo número de linhas para todas as colunas, e a serie_longa ditou que o varal tem 4 posições, o pandas preencheu as posições vazias da serie_curta com esse "fantasma".


# ## Exercício 5: O Comportamento do Jupyter
# Vamos testar aquela "viadagem" do Jupyter exibir coisas sem o print().
# %%
texto1 = "Estou invisível"
texto2 = "Eu apareço!"

# DESAFIO:
# 1. Coloque 'texto1' e 'texto2' em linhas separadas no final desta célula, sem usar o print().
texto1
texto2
# %%
# 2. Rode a célula. Quem apareceu na tela do lado direito?
# somente o texto 2

# 3. Agora envolva os dois em funções print() e rode de novo para ver a diferença.
print(texto1, texto2)

# Explicacao: No Jupyter, apenas o resultado da última linha da célula é exibido automaticamente, para ver qualquer coisa antes dela, você precisa usar o print().
# A ideia é que, quando você está analisando dados, você quer ver o resultado de uma operação (como o topo de uma tabela ou o valor de uma conta) instantaneamente, sem precisar digitar print() o tempo todo.


# ## Exercício 6: O Filtro "Bouncer" (Booleano)
idades = pd.Series([15, 22, 12, 45, 18, 30])

# DESAFIO:
# 1. Crie uma variável chamada 'maiores' que receba: idades >= 18
maiores = idades >= 18

# 2. Imprima essa variável. O que apareceu? 
print(maiores)
# apenas valores booleanos, True e False

# 3. Agora tente imprimir: idades[maiores]
print(idades[maiores]) 
# imprimou os valores das idades, e nao valores booleanos


# ## Exercício 7: Localizando com .loc (O Nome importa)
df_precos = pd.DataFrame({
    'produto': ['Teclado', 'Mouse', 'Monitor'],
    'valor': [150, 80, 900]
}, index=['p1', 'p2', 'p3'])

# DESAFIO:
# 1. Use o .loc para pegar APENAS o valor do 'Mouse'.
print(df_precos.loc['p2'])

# 2. Tente pegar todos os valores de p1 a p2 usando .loc.
print(df_precos.loc['p1':'p2'])


# ## Exercício 8: Adicionando "Roupas" no Varal
df_loja = pd.DataFrame({
    'custo': [10, 20, 30],
    'nome': ['caneta', 'lápis', 'caderno']
})

# DESAFIO:
# 1. Crie uma nova coluna chamada 'venda' que seja o dobro do custo.
df_loja['venda'] = df_loja['custo'] * 2
print(df_loja)


# ## Exercício 9: O Reset de Fábrica (reset_index)
series_baguncada = pd.Series([10, 5, 20], index=['b', 'a', 'c']).sort_values()

# DESAFIO:
# 1. Imprima a series. Veja o índice 'a' no topo.
print(series_baguncada)

# 2. Use o comando: series_baguncada.reset_index(drop=True)
print(series_baguncada.reset_index(drop=True))

# 3. O que aconteceu com o índice?
# ele trocou as keys de 'a', 'b' e 'c' e por indices de 0 a diante


# ## Exercício 10: Contando as Peças
generos = pd.Series(['Ação', 'Comédia', 'Ação', 'Drama', 'Ação', 'Comédia'])

# DESAFIO:
# 1. Use o comando: generos.value_counts()
print(generos.value_counts())

# 2. O que esse comando faz?
# ele conta a quantidade de cada genero e retorna em ordem decrescente