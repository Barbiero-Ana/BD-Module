import sqlite3
from clientes import cadastrar_cliente, listar_clientes, buscar_cliente_por_id
from gestao import adicionar_prato, listar_pratos, atualizar_prato, gerar_relatorio_vendas, listar_pedidos, alterar_status_pedido
from vendas import registrar_pedido, enviar_email_confirmacao
from emailsender import enviar_email_cupom
from dotenv import load_dotenv
import os

load_dotenv()


senha_gestor = os.getenv('SENHA_GESTOR')
senha_atendente = os.getenv('SENHA_ATENDENTE')






# Função de login (gerente ou atendente)
def login():
    print("Bem-vindo ao sistema de restaurante!")
    usuario = input("Usuário: ")
    senha = input("Senha: ")
    
    if usuario == "gestor" and senha == senha_gestor:
        return "gestor"
    elif usuario == "atendente" and senha == senha_atendente:
        return "atendente"
    else:
        print("Credenciais inválidas. Tente novamente.")
        return None

def menu_gestor():
    while True:
        print("\n1. Adicionar Prato\n2. Listar Pratos\n3. Atualizar Preço do Prato\n4. Gerar Relatório de Vendas\n5. Enviar Cupom de Desconto\n6. Listar Pedidos\n7. Alterar Status de Pedido\n8. Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            nome = input("Nome do prato: ")
            preco = float(input("Preço do prato: "))
            adicionar_prato(nome, preco)

        elif opcao == "2":
            listar_pratos()

        elif opcao == "3":
            prato_id = int(input("ID do prato: "))
            novo_preco = float(input("Novo preço: "))
            atualizar_prato(prato_id, novo_preco)

        elif opcao == "4":
            gerar_relatorio_vendas()

        elif opcao == "5":
            cliente_id = int(input("ID do cliente: "))
            cupom_codigo = input("Código do cupom de desconto: ")
            cliente = buscar_cliente_por_id(cliente_id)
            if cliente:
                enviar_email_cupom(cliente[2], cupom_codigo)

        elif opcao == "6":
            listar_pedidos()

        elif opcao == "7":
            alterar_status_pedido()

        elif opcao == "8":
            print("Saindo...")
            break

        else:
            print("Opção inválida!")

def menu_atendente():
    while True:
        print("\n1. Registrar Pedido\n2. Listar Clientes\n3. Cadastrar cliente\n4. Listar pratos\n5. Sair")
        opcao = int(input("Escolha uma opção: "))

        if opcao == 1:

            #dando print dos usuarios já cadastrados pra poder pegar a ID

            conexao = sqlite3.connect("restaurante.db")
            cursor = conexao.cursor()

            cursor.execute("SELECT * FROM clientes")
            clientes = cursor.fetchall()
            conexao.close()
            print("\nLista de Clientes:")
            for cliente in clientes:
                print(f"ID: {cliente[0]} | Nome: {cliente[1]} | E-mail: {cliente[2]}")


            cliente_id = int(input("\nID do cliente: "))

            # dando print dos pratos que já estão cadastrados

            conexao = sqlite3.connect("restaurante.db")
            cursor = conexao.cursor()
            
            cursor.execute("SELECT * FROM pratos")
            pratos = cursor.fetchall()
            
            conexao.close()
            
            if not pratos:
                print("Nenhum prato cadastrado.")
            else:
                print("Lista de Pratos:")
                for prato in pratos:
                    print(f"ID: {prato[0]}, Nome: {prato[1]}, Preço: R$ {prato[2]:.2f}")

            pratos = [int(input("\nID do prato: "))]
            quantidade = [int(input("Quantidade do prato: "))]
            registrar_pedido(cliente_id, pratos, quantidade)
            conexao = sqlite3.connect("restaurante.db")
            cursor = conexao.cursor()
            cursor.execute("SELECT email FROM clientes WHERE id = ?", (cliente_id,))
            resultado = cursor.fetchone()
            conexao.close()

            if resultado:
                email_cliente = resultado[0]
                
                # Calcular o valor total do pedido
                conexao = sqlite3.connect("restaurante.db")
                cursor = conexao.cursor()
                cursor.execute("SELECT preco FROM pratos WHERE id = ?", (pratos[0],))
                preco_prato = cursor.fetchone()
                conexao.close()

                if preco_prato:
                    total = preco_prato[0] * quantidade[0]
                else:
                    total = 0
                    
                enviar_email_confirmacao(email_cliente, pratos, quantidade, total)
            else:
                print("Erro: Cliente não encontrado.")

        elif opcao == 2:
            listar_clientes()
        
        elif opcao == 3:
            nome = input("Nome do cliente: ")
            email = input("E-mail do cliente: ")

            # ACHEI O MALDITO ERRO
            cadastrar_cliente(nome, email)

        elif opcao == 4:
            listar_pratos()

        elif opcao == 5:
            print("Saindo...")
            break

        else:
            print("Opção inválida!")


if __name__ == "__main__":
    while True:
        tipo_usuario = login()
        
        if tipo_usuario == "gestor":
            menu_gestor()
        elif tipo_usuario == "atendente":
            menu_atendente()
        else:
            continue
