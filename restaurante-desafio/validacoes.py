'''
modulo somente de validacoes para import em outros códigos

'''

import re
from datetime import datetime



def validar_telefone(telefone):
    numeros = re.sub(r'\D', '', telefone)
    if len(numeros) == 11:
        return f'({numeros[:2]}) {numeros[2:7]}-{numeros[7:]}'
    elif len(numeros) == 10:
        return f'({numeros[:2]}) {numeros[2:6]}-{numeros[6:]}'
    else:
        return telefone

def validar_email(email):
    padrao = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(padrao, email) is not None


def validar_isbn(isbn):
    isbn = re.sub(r'\D', '', isbn)  # Remove caracteres não numéricos
    
    if len(isbn) == 10:
        soma = sum((i + 1) * int(digito) for i, digito in enumerate(isbn[:-1]))
        ultimo_digito = 10 if isbn[-1] == 'X' else int(isbn[-1])
        return soma % 11 == ultimo_digito

    elif len(isbn) == 13:
        soma = sum((1 if i % 2 == 0 else 3) * int(digito) for i, digito in enumerate(isbn))
        return soma % 10 == 0

    return False

def validar_cpf(cpf):
    cpf = re.sub(r'\D', '', cpf)  # Remove caracteres não numéricos

    if len(cpf) != 11 or cpf == cpf[0] * 11:  # Verifica tamanho e CPFs inválidos (111.111.111-11 etc.)
        return False

    # Cálculo do primeiro dígito verificador
    soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
    resto = soma % 11
    primeiro_digito = 0 if resto < 2 else 11 - resto

    # Cálculo do segundo dígito verificador
    soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
    resto = soma % 11
    segundo_digito = 0 if resto < 2 else 11 - resto

    # Verifica se os dígitos calculados são iguais aos do CPF informado
    return cpf[-2:] == f"{primeiro_digito}{segundo_digito}"


def validar_data_nascimento(data):
    try:
        # Converte a string em data
        data_nasc = datetime.strptime(data, "%d/%m/%Y")
        
        # Obtém a data atual
        hoje = datetime.today()
        
        # Calcula a idade
        idade = hoje.year - data_nasc.year - ((hoje.month, hoje.day) < (data_nasc.month, data_nasc.day))

        # Valida se a idade está dentro de um intervalo realista
        if 0 < idade < 120:
            return True
        else:
            return False
    except ValueError:
        return False  # Retorna falso se a conversão falhar


def validar_cep(cep):
    # Remover caracteres não numéricos
    cep = re.sub(r"\D", "", cep)

    # Verificar se tem exatamente 8 dígitos
    return len(cep) == 8 and cep.isdigit()

