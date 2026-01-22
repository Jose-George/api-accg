import re

def validar_cpf(cpf):
    """ Valida um número de CPF conforme algoritmo oficial """
    # Remove caracteres não numéricos
    cpf = re.sub(r'\D', '', str(cpf))

    if len(cpf) != 11 or cpf == cpf[0] * 11:
        return False

    # Cálculo dos dígitos verificadores
    for i in range(9, 11):
        soma = sum(int(cpf[num]) * ((i + 1) - num) for num in range(i))
        digito = (soma * 10 % 11) % 10
        if digito != int(cpf[i]):
            return False
    return True

def validar_cnpj(cnpj):
    """ Valida um número de CNPJ conforme algoritmo oficial """
    # Remove caracteres não numéricos
    cnpj = re.sub(r'\D', '', str(cnpj))

    if len(cnpj) != 14 or cnpj == cnpj[0] * 14:
        return False

    # Pesos para o cálculo
    def calcular_digito(fatia, pesos):
        soma = sum(int(a) * b for a, b in zip(fatia, pesos))
        resto = soma % 11
        return 0 if resto < 2 else 11 - resto

    pesos1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    pesos2 = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]

    digito1 = calcular_digito(cnpj[:12], pesos1)
    digito2 = calcular_digito(cnpj[:13], pesos2)

    return cnpj[-2:] == f"{digito1}{digito2}"