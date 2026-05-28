# %%
import pandas as pd

df = pd.DataFrame({
    "cliente": [1,2,3,4,5],
    "nome": ["teo", "jose", "nah", "mah", "lah"],
})

df_02 = pd.DataFrame({
    "cliente": [6,7,8],
    "nome": ["kozato", "laura", "dan",],
    "idade":[32,29,31],
})

df_03 = pd.DataFrame({
    "idade": [32,34,19,54,33]
})


# %% 
dfs = [df, df_02]
pd.concat(dfs, ignore_index=True)


# %%
# por padrao o concat coloca um df em cima do outro empilhando ele, para evitar isso usasse o 'axis'
pd.concat([df, df_03], axis=1)