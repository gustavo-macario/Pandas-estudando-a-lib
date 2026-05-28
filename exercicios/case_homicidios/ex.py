# %%
import pandas as pd
import os

# %%
# 1
caminho_pasta = "../../data2/"
arquivos_na_pasta = os.listdir(caminho_pasta)

# %%
# 2
def limpar_nome_arquivo(nome_arquivo):
    nome_limpo, extensao = os.path.splitext(nome_arquivo)
    nome_limpo = nome_limpo.replace(" (1)", "")
    return nome_limpo

# %%
# 3
def carregar_e_preparar(nome_arquivo):
    caminho_completo = os.path.join("../../data2/", nome_arquivo)
    df = pd.read_excel(caminho_completo)
    df['categoria'] = limpar_nome_arquivo(nome_arquivo)
    return df


# %%
# 4
lista_dfs = []

for arquivo in arquivos_na_pasta:
    if arquivo.endswith('.xlsx'):
        df_temporario = carregar_e_preparar(arquivo)
        lista_dfs.append(df_temporario)


# %%
# 5
df_consolidado = pd.concat(lista_dfs, axis=0, ignore_index=True)


# %%
# 6
print(df_consolidado.head())
print(f"Tamanho: {df_consolidado.shape}")
print(df_consolidado.dtypes)


# %%
# 7
ano_min = df_consolidado['período'].min()
ano_max = df_consolidado['período'].max()
print(f"Dados de {ano_min} até {ano_max}")


# %%
# 8
df_sp_recente = df_consolidado[(df_consolidado['nome'] == 'SP') & (df_consolidado['período'] == 2021)]
print(df_sp_recente)


# %%
# 9
df_consolidado.to_csv("base_consolidada.csv", index=False)