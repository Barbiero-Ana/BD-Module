import sqlite3
import hashlib
import re

def hash_senha(senha):
    return hashlib.sha256(senha.encode()).hexdigest()

def validar_email(email):
    padrao = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(padrao, email) is not None


def login(email, senha):
    conexao = sqlite3.connect("restaurante.db")
    cursor = conexao.cursor()

    cursor.execute("SELECT id, nome, cargo, senha FROM usuarios WHERE email = ?", (email,))
    usuario = cursor.fetchone()
    conexao.close()

    if usuario and usuario[3] == hash_senha(senha):
        print(f"Login bem-sucedido! Bem-vindo, {usuario[1]} ({usuario[2]}).")
        return usuario
    else:
        print("E-mail ou senha incorretos.")
        return None






