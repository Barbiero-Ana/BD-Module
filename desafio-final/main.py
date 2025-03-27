import sqlite3
from clientes import cadastrar_cliente, listar_clientes, buscar_cliente_por_id
from gestao import adicionar_prato, listar_pratos, atualizar_prato, gerar_relatorio_vendas, listar_pedidos, alterar_status_pedido
from vendas import registrar_pedido
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
            cliente_id = int(input("ID do cliente: "))
            pratos = [int(input("ID do prato: "))]
            quantidade = [int(input("Quantidade do prato: "))]
            registrar_pedido(cliente_id, pratos, quantidade)

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
