import pandas as pd
import os
import unidecode 
os.makedirs("data", exist_ok=True)

caminho_arquivo = "data/Taco-4a-Edicao.xlsx"


df = pd.read_excel('/home/joao/nutribot_ai/data/Taco-4a-Edicao.xlsx', sheet_name='CMVCol taco3', skiprows=3)


df.columns.values[0] = "grupo"
df.columns.values[1] = "alimento"
df.columns.values[3] = "calorias"
df.columns.values[5] = "proteinas"
df.columns.values[10] = "carboidratos"
df.columns.values[6] = "gorduras"


df = df[["alimento", "calorias", "proteinas", "carboidratos", "gorduras"]].copy()


df.insert(1, "porcao_gramas", 100)

df.replace(["–", "-", "", " "], pd.NA, inplace=True)


colunas = ["calorias", "proteinas", "carboidratos", "gorduras"]
df[colunas] = df[colunas].apply(pd.to_numeric, errors="coerce")


df.dropna(subset=colunas, inplace=True)


df[colunas] = df[colunas].round(2)

df["alimento"] = df["alimento"].apply(lambda x: unidecode.unidecode(str(x)).replace(",", "").strip())

df.reset_index(drop=True, inplace=True)

os.makedirs("data", exist_ok=True)


caminho_csv = os.path.join(os.path.dirname(__file__), "../../data/alimentos.csv")
df.to_csv(caminho_csv, index=False)

print("✅ CSV salvo com sucesso em:", caminho_csv)
