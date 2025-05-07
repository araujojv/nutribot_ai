import pandas as pd
import os
import unidecode 
os.makedirs("data", exist_ok=True)

caminho_arquivo = "data/Taco-4a-Edicao.xlsx"

# Carregar a aba principal e pular os cabeçalhos extras
df = pd.read_excel('/home/joao/nutribot_ai/data/Taco-4a-Edicao.xlsx', sheet_name='CMVCol taco3', skiprows=3)

# Renomear as colunas que vamos usar
df.columns.values[0] = "grupo"
df.columns.values[1] = "alimento"
df.columns.values[3] = "calorias"
df.columns.values[5] = "proteinas"
df.columns.values[10] = "carboidratos"
df.columns.values[6] = "gorduras"

# Selecionar apenas as colunas úteis
df = df[["alimento", "calorias", "proteinas", "carboidratos", "gorduras"]].copy()

# Adicionar coluna de porção padrão
df.insert(1, "porcao_gramas", 100)

# Substituir valores inválidos (ex: traço) por NaN
df.replace(["–", "-", "", " "], pd.NA, inplace=True)

# Converter para float, ignorando erros
colunas = ["calorias", "proteinas", "carboidratos", "gorduras"]
df[colunas] = df[colunas].apply(pd.to_numeric, errors="coerce")

# Remover linhas incompletas
df.dropna(subset=colunas, inplace=True)

# Arredondar os valores
df[colunas] = df[colunas].round(2)

df["alimento"] = df["alimento"].apply(lambda x: unidecode.unidecode(str(x)).replace(",", "").strip())

# Resetar índice
df.reset_index(drop=True, inplace=True)
# Cria a pasta se não existir
os.makedirs("data", exist_ok=True)

# Caminho absoluto para salvar
caminho_csv = os.path.join(os.path.dirname(__file__), "../../data/alimentos.csv")
df.to_csv(caminho_csv, index=False)

print("✅ CSV salvo com sucesso em:", caminho_csv)
