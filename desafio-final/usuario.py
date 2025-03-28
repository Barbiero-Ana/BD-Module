import sqlite3
import hashlib
import re

def hash_senha(senha):
    return hashlib.sha256(senha.encode()).hexdigest()

def validar_email(email):
    padrao = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(padrao, email) is not None

def cadastrar_usuario(nome, cargo, email, senha):
    if cargo not in ['gestor', 'atendente']:
        print("Cargo inválido! Escolha entre 'gestor' ou 'atendente'.")
        return
    
    if not validar_email(email):
        print("E-mail inválido!")
        return

    conexao = sqlite3.connect("restaurante.db")
    cursor = conexao.cursor()

    try:
        cursor.execute("INSERT INTO usuarios (nome, cargo, email, senha) VALUES (?, ?, ?, ?)", 
                    (nome, cargo, email, hash_senha(senha)))
        conexao.commit()
        print(f"{cargo.capitalize()} cadastrado com sucesso!")
    except sqlite3.IntegrityError:
        print("Erro: E-mail já cadastrado.")
    
    conexao.close()

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

if __name__ == "__main__":
    while True:
        print("\n1. Cadastrar usuário\n2. Fazer login\n3. Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            nome = input("Nome: ")
            cargo = input("Cargo (gestor/atendente): ").strip().lower()
            email = input("E-mail: ").strip()
            senha = input("Senha: ")
            cadastrar_usuario(nome, cargo, email, senha)
        
        elif opcao == "2":
            email = input("E-mail: ").strip()
            senha = input("Senha: ")
            login(email, senha)

        elif opcao == "3":
            print("Saindo...")
            break

        else:
            print("Opção inválida!")
