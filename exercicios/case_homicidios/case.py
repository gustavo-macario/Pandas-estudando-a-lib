# %% 
import pandas as pd
import os 
# %%
def read_file(file_name:str):
    df= (pd.read_excel(f'../../data2/{file_name}.xlsx')
         .rename(columns={"valor":file_name})
         .set_index(["nome", "período"])
         .drop(["cod"], axis=1))
    
    return df

# %%
file_names = os.listdir("../../data2/")

dfs = []
for i in file_names:
    file_name = i.split(".")[0]
    dfs.append(read_file(file_name))

dfs[-3]



# %%
df_full = (pd.concat(dfs, axis=1).reset_index())
df_full
# %%
