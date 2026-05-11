# %%
import pandas as pd

url = "https://pt.wikipedia.org/wiki/Unidades_federativas_do_Brasil"

dfs = pd.read_html(url)
uf = dfs[1]

