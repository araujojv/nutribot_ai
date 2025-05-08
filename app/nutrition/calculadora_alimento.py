import pandas as pd
import unidecode
import difflib

def encontrar_alimento(df, nome_digitado):
    nome_normalizado = unidecode.unidecode(nome_digitado.lower().strip())
    alimentos_normalizados = df["alimento"].apply(lambda x: unidecode.unidecode(x.lower().strip())).tolist()
    sugestoes = difflib.get_close_matches(nome_normalizado, alimentos_normalizados, n=1, cutoff=0.7)

    if sugestoes:
        idx = alimentos_normalizados.index(sugestoes[0])
        return df.iloc[idx]
    else:
        return None


def calcular_refeicao(lista_alimentos):
    df = pd.read_csv("data/alimentos.csv")

    totais = {
        "calorias": 0,
        "proteinas": 0,
        "carboidratos": 0,
        "gorduras": 0
    }

    detalhes = []

    for item in lista_alimentos:
        nome = item["alimento"]
        gramas = item["gramas"]

        linha = encontrar_alimento(df, nome)

        if linha is None:
            detalhes.append({"alimento": nome, "erro": "Não encontrado"})
            continue

        fator = gramas / linha['porcao_gramas']

        resultado = {
            "alimento": linha['alimento'],
            "quantidade": gramas,
            "calorias": round(linha['calorias'] * fator, 2),
            "proteinas": round(linha['proteinas'] * fator, 2),
            "carboidratos": round(linha['carboidratos'] * fator, 2),
            "gorduras": round(linha['gorduras'] * fator, 2)
        }

        totais["calorias"] += resultado["calorias"]
        totais["proteinas"] += resultado["proteinas"]
        totais["carboidratos"] += resultado["carboidratos"]
        totais["gorduras"] += resultado["gorduras"]

        detalhes.append(resultado)

    return {
        "detalhes": detalhes,
        "totais": {k: round(v, 2) for k, v in totais.items()}
    }
