import sqlite3
import re

# Função para validar o e-mail
def validar_email(email):
    padrao = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(padrao, email) is not None

# Função para cadastrar cliente
def cadastrar_cliente(nome, email):
    if not validar_email(email):
        print("E-mail inválido!")
        return

    conexao = sqlite3.connect("restaurante.db")
    cursor = conexao.cursor()

    try:
        cursor.execute("INSERT INTO clientes (nome, email) VALUES (?, ?)", (nome, email,))
        conexao.commit()
        print(f"Cliente '{nome}' cadastrado com sucesso!")
    except sqlite3.IntegrityError:
        print("Erro: E-mail já cadastrado.")
    
    conexao.close()

def buscar_cliente_por_id(cliente_id):
    conexao = sqlite3.connect("restaurante.db")
    cursor = conexao.cursor()

    cursor.execute("SELECT * FROM clientes WHERE id = ?", (cliente_id,))
    cliente = cursor.fetchone()
    conexao.close()

    return cliente

def listar_clientes():
    conexao = sqlite3.connect("restaurante.db")
    cursor = conexao.cursor()

    cursor.execute("SELECT * FROM clientes")
    clientes = cursor.fetchall()
    conexao.close()

    print("\nLista de Clientes:")
    for cliente in clientes:
        print(f"ID: {cliente[0]} | Nome: {cliente[1]} | E-mail: {cliente[2]}")

if __name__ == "__main__":
    while True:
        print("\n1. Cadastrar Cliente\n2. Listar Clientes\n3. Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            nome = input("Nome do cliente: ")
            email = input("E-mail do cliente: ")
            cadastrar_cliente(nome, email)

        elif opcao == "2":
            listar_clientes()

        elif opcao == "3":
            print("Saindo...")
            break

        else:
            print("Opção inválida!")
