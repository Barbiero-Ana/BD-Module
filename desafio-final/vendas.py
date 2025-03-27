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


def registrar_pedido(cliente_id, pratos, quantidade):
    conexao = sqlite3.connect("restaurante.db")
    cursor = conexao.cursor()

    # Calculando o valor total do pedido
    total = 0
    for prato_id, qtd in zip(pratos, quantidade):
        cursor.execute("SELECT preco FROM pratos WHERE id = ?", (prato_id,))
        preco = cursor.fetchone()[0]
        total += preco * qtd
    
    
    cursor.execute('''
        INSERT INTO vendas_pedidos (cliente_id, prato_id, quantidade, total, status)
        VALUES (?, ?, ?, ?, 'pendente')
    ''', (cliente_id, pratos[0], quantidade[0], total))  # Apenas exemplo para 1 prato

    conexao.commit()
    conexao.close()

    print(f"Pedido registrado para o cliente {cliente_id} com status 'pendente'.")


# enviar o maldito email de confirmacao - que funcione plmds

def enviar_email_confirmacao(email_cliente, pratos, quantidade, total):
    email_remetente = user_email
    senha_remetente = user_password
    smtp_server = "smtp.gmail.com"
    smtp_port = 587

    # Criando a mensagem
    mensagem = MIMEMultipart()
    mensagem['From'] = email_remetente
    mensagem['To'] = email_cliente
    mensagem['Subject'] = "Confirmação de Pedido"

    corpo_email = f"""
    Olá, seu pedido foi confirmado! Detalhes do pedido:

    Pratos solicitados:
    """
    
    for prato, quantid in zip(pratos, quantidade):
        corpo_email += f"Prato ID: {prato} | Quantidade: {quantid}\n"
    
    corpo_email += f"\nTotal: R$ {total:.2f}\n\nAguarde a confirmação do status de entrega.\n\nObrigado por escolher nosso restaurante!"

    mensagem.attach(MIMEText(corpo_email, 'plain'))

    try:

        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(email_remetente, senha_remetente)

        
        server.sendmail(email_remetente, email_cliente, mensagem.as_string())
        server.quit()
        print("E-mail de confirmação enviado com sucesso!")
    except Exception as e:
        print(f"Erro ao enviar o e-mail: {e}")

if __name__ == "__main__":
    while True:
        print("\n1. Registrar Pedido\n2. Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            cliente_id = int(input("ID do cliente: "))
            pratos = [int(input("ID do prato: "))]
            quantidade = [int(input("Quantidade do prato: "))]
            registrar_pedido(cliente_id, pratos, quantidade)

        elif opcao == "2":
            print("Saindo...")
            break

        else:
            print("Opção inválida!")
