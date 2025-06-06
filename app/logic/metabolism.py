def calcular_tmb(peso,altura,idade,sexo):
    if sexo.lower() == 'masculino':
        return 10 * peso + 6.25 * altura - 5 * idade + 5
    else:
        return 10 * peso + 6.25 * altura - 5 * idade - 161
    
def calcular_tdee(tmb, nivel_atividade):
    fatores = {
        'sedentario': 1.2,
        'leve': 1.375,
        'moderado': 1.55,
        'intenso': 1.725,
        'muito_intenso': 1.9
    }
    return tmb* fatores.get(nivel_atividade,1.2)