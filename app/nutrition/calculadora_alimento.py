import pandas as pd

def calcular_refeicao(lista_alimentos):
    df = pd.read_csv("/home/joao/nutribot_ai/data/Taco-4a-Edicao.xlsx")

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

        alimento = df[df['alimento'].str.lower() == nome.lower()]

        if alimento.empty:
            detalhes.append({"alimento": nome, "erro": "Não encontrado"})
            continue

        linha = alimento.iloc[0]
        fator = gramas / linha['porcao_gramas']

        resultado = {
            "alimento": nome,
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
