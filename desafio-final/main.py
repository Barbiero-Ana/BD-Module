import sqlite3
from clientes import cadastrar_cliente, listar_clientes, buscar_cliente_por_id
from gestao import adicionar_prato, listar_pratos, atualizar_prato, gerar_relatorio_vendas, listar_pedidos, alterar_status_pedido, excluir_prato
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
        print("\n1. Adicionar Prato\n2. Listar Pratos\n3. Atualizar Preço do Prato\n4. Gerar Relatório de Vendas\n5. Enviar Cupom de Desconto\n6. Listar Pedidos\n7. Alterar Status de Pedido\n8. Remover prato\n9. Sair")
        opcao = int(input("Escolha uma opção: "))

        if opcao == 1:
            nome = input("Nome do prato: ")
            preco = float(input("Preço do prato: "))
            adicionar_prato(nome, preco)

        elif opcao == 2:
            listar_pratos()

        elif opcao == 3:
            prato_id = int(input("ID do prato: "))
            novo_preco = float(input("Novo preço: "))
            atualizar_prato(prato_id, novo_preco)

        elif opcao == 4:
            gerar_relatorio_vendas()

        elif opcao == 5:
            # Listar clientes
            conexao = sqlite3.connect("restaurante.db")
            cursor = conexao.cursor()
            cursor.execute("SELECT * FROM clientes")
            clientes = cursor.fetchall()
            conexao.close()

            print("\nLista de Clientes:")
            for cliente in clientes:
                print(f"ID: {cliente[0]} | Nome: {cliente[1]} | E-mail: {cliente[2]}")

            cliente_id = int(input("ID do cliente: "))
            cupom_codigo = input("Código do cupom de desconto: ")
            cliente = buscar_cliente_por_id(cliente_id)
            if cliente:
                enviar_email_cupom(cliente[2], cupom_codigo)

        elif opcao == 6:
            listar_pedidos()

        elif opcao == 7:
            alterar_status_pedido()

        elif opcao == 8:
            # Listar pratos cadastrados
            conexao = sqlite3.connect("restaurante.db")
            cursor = conexao.cursor()
            cursor.execute("SELECT * FROM pratos")
            pratos_disponiveis = cursor.fetchall()
            conexao.close()

            if not pratos_disponiveis:
                print("Nenhum prato cadastrado.")
                continue  

            print("\nLista de Pratos:")
            for prato in pratos_disponiveis:
                print(f"ID: {prato[0]} | Nome: {prato[1]} | Preço: R$ {prato[2]:.2f}")

            try:
                prato_id = int(input("Digite o ID do prato a ser excluído: "))
                excluir_prato(prato_id)
            except ValueError:
                print("Erro: Digite um número válido para o ID do prato.")

        elif opcao == 9:
            print("Saindo...")
            break

        else:
            print("Opção inválida!")

def menu_atendente():
    while True:
        print("\n1. Registrar Pedido\n2. Listar Clientes\n3. Cadastrar Cliente\n4. Listar Pratos\n5. Sair")
        opcao = int(input("Escolha uma opção: "))

        if opcao == 1:
            # Listar clientes
            conexao = sqlite3.connect("restaurante.db")
            cursor = conexao.cursor()
            cursor.execute("SELECT * FROM clientes")
            clientes = cursor.fetchall()
            conexao.close()

            print("\nLista de Clientes:")
            for cliente in clientes:
                print(f"ID: {cliente[0]} | Nome: {cliente[1]} | E-mail: {cliente[2]}")

            cliente_id = int(input("\nID do cliente: "))

            # busca o email do cliente
            conexao = sqlite3.connect("restaurante.db")
            cursor = conexao.cursor()
            cursor.execute("SELECT email FROM clientes WHERE id = ?", (cliente_id,))
            resultado = cursor.fetchone()
            conexao.close()

            if not resultado:
                print("Erro: Cliente não encontrado.")
                continue  

            email_cliente = resultado[0]

            
            conexao = sqlite3.connect("restaurante.db")
            cursor = conexao.cursor()
            cursor.execute("SELECT * FROM pratos")
            pratos_disponiveis = cursor.fetchall()
            conexao.close()

            if not pratos_disponiveis:
                print("Nenhum prato cadastrado.")
                continue  

            print("\nLista de Pratos:")
            for prato in pratos_disponiveis:
                print(f"ID: {prato[0]} | Nome: {prato[1]} | Preço: R$ {prato[2]:.2f}")

            
            pratos = []
            quantidades = []
            total_pedido = 0

            while True:
                prato_id = input("\nAperte enter para confirmar").strip()
                if not prato_id:
                    break  

                prato_id = int(prato_id)
                quantidade = int(input("Quantidade do prato: "))

                for prato in pratos_disponiveis:
                    if prato[0] == prato_id:
                        pratos.append(prato[1])  
                        quantidades.append(quantidade)
                        total_pedido += prato[2] * quantidade
                        break
                else:
                    print("Prato não encontrado.")

            if not pratos:
                print("Nenhum prato selecionado. Pedido cancelado.")
                continue  

            
            registrar_pedido(cliente_id, pratos, quantidades)

            # Enviar email de confirmacao ao receber o status como pronto
            enviar_email_confirmacao(email_cliente, pratos, quantidades, total_pedido)

        elif opcao == 2:
            listar_clientes()

        elif opcao == 3:
            nome = input("Nome do cliente: ")
            email = input("E-mail do cliente: ")
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
