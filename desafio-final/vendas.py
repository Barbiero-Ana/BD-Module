import sqlite3
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os

load_dotenv()

user_email = os.getenv('USER_EMAIL')
user_password = os.getenv('USER_PASSWORD')

def buscar_cliente_por_id(cliente_id):
    conexao = sqlite3.connect("restaurante.db")
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM clientes WHERE id = ?", (cliente_id,))
    cliente = cursor.fetchone()
    conexao.close()
    return cliente  

def registrar_pedido(cliente_id, pratos, quantidades):
    conexao = sqlite3.connect("restaurante.db")
    cursor = conexao.cursor()

    total_pedido = 0

    for prato, quantidade in zip(pratos, quantidades):
        cursor.execute("SELECT preco FROM pratos WHERE nome = ?", (prato,))
        preco = cursor.fetchone()[0]
        subtotal = preco * quantidade
        total_pedido += subtotal

        cursor.execute('''
            INSERT INTO vendas_pedidos (cliente_id, prato_id, quantidade, total, status)
            VALUES (?, ?, ?, ?, 'pendente')
        ''', (cliente_id, prato, quantidade, subtotal))

    conexao.commit()
    conexao.close()

    print(f"Pedido registrado para o cliente {cliente_id} com status 'pendente'.")
    return total_pedido

def enviar_email_confirmacao(email_cliente, pratos, quantidades, total):
    email_remetente = user_email
    senha_remetente = user_password
    smtp_server = "smtp.gmail.com"
    smtp_port = 587

    mensagem = MIMEMultipart()
    mensagem['From'] = email_remetente
    mensagem['To'] = email_cliente
    mensagem['Subject'] = "Confirmação de Pedido"

    corpo_email = "Olá, seu pedido foi confirmado! Detalhes do pedido:\n\nPratos solicitados:\n"

    for prato, quantidade in zip(pratos, quantidades):
        corpo_email += f"{prato} | Quantidade: {quantidade}\n"

    corpo_email += f"\n**Total do Pedido: R$ {total:.2f}**\n\nAguarde a confirmação do status de entrega.\n\nObrigado por escolher nosso restaurante!"

    mensagem.attach(MIMEText(corpo_email, 'plain'))

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(email_remetente, senha_remetente)
        server.sendmail(email_remetente, email_cliente, mensagem.as_string())
        server.quit()
        print("E-mail enviado com sucesso!")
    except Exception as e:
        print(f"Erro ao enviar o e-mail: {e}")

if __name__ == "__main__":
    while True:
        print("\n1. Registrar Pedido\n2. Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            cliente_id = int(input("ID do cliente: "))

            # Buscar e-mail do cliente
            conexao = sqlite3.connect("restaurante.db")
            cursor = conexao.cursor()
            cursor.execute("SELECT email FROM clientes WHERE id = ?", (cliente_id,))
            resultado = cursor.fetchone()
            conexao.close()

            if not resultado:
                print("Erro: Cliente não encontrado.")
                continue

            email_cliente = resultado[0]

            # Registrar múltiplos pratos
            pratos = []
            quantidades = []

            conexao = sqlite3.connect("restaurante.db")
            cursor = conexao.cursor()
            cursor.execute("SELECT nome, preco FROM pratos")
            pratos_disponiveis = cursor.fetchall()
            conexao.close()

            print("\nLista de Pratos:")
            for idx, (nome, preco) in enumerate(pratos_disponiveis, start=1):
                print(f"{idx}. {nome} - R$ {preco:.2f}")

            while True:
                prato_escolhido = input("\nNome do prato (ou ENTER para finalizar): ").strip()
                if not prato_escolhido:
                    break
                quantidade = int(input("Quantidade do prato: "))

                pratos.append(prato_escolhido)
                quantidades.append(quantidade)

            if not pratos:
                print("Nenhum prato selecionado. Pedido cancelado.")
                continue

            # Registrar pedido e calcular total
            total_pedido = registrar_pedido(cliente_id, pratos, quantidades)

            # Enviar e-mail de confirmação
            enviar_email_confirmacao(email_cliente, pratos, quantidades, total_pedido)

        elif opcao == "2":
            print("Saindo...")
            break

        else:
            print("Opção inválida!")