def calcular_tbm(peso,altura,idade,sexo):
    if sexo.lower() == 'masculino':
        return 10 * peso + 6.25 * altura - 5 * idade + 5
    else:
        return 10 * peso + 6.25 * altura - 5 * idade - 161