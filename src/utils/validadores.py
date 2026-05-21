def validar_inteiro(texto):
    if texto.isdigit() and int(texto) > 0:
        return True
    return "Por favor, digite um número inteiro maior que zero."

def validar_float(texto):
    try:
        valor = float(texto)
        if 0.0 <= valor <= 1.0:
            return True
        return "O valor deve estar entre 0.0 e 1.0."
    except ValueError:
        return "Por favor, digite um número decimal válido (ex: 0.15)."
    
def validar_inteiro_ou_vazio(texto):
    if texto == "": return True  # Libera o Enter
    if texto.isdigit() and int(texto) > 0: return True
    return "Digite um número inteiro maior que zero."

def validar_float_ou_vazio(texto):
    if texto == "": return True  # Libera o Enter
    try:
        valor = float(texto)
        if 0.0 <= valor <= 1.0: return True
        return "O valor deve estar entre 0.0 e 1.0."
    except ValueError:
        return "Digite um decimal válido (ex: 0.15)."