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
    pratos_nomes = []  # Para armazenar os nomes dos pratos para o e-mail

    for prato, quantidade in zip(pratos, quantidades):
        
        cursor.execute("SELECT id, preco FROM pratos WHERE nome = ?", (prato,))
        resultado = cursor.fetchone()
        if not resultado:
            print(f"Prato '{prato}' não encontrado na tabela pratos.")
            continue
        prato_id, preco = resultado
        subtotal = preco * quantidade
        total_pedido += subtotal
        pratos_nomes.append(prato)  

        
        cursor.execute('''
            INSERT INTO vendas_pedidos (cliente_id, prato_id, quantidade, total, status)
            VALUES (?, ?, ?, ?, 'pendente')
        ''', (cliente_id, prato_id, quantidade, subtotal))

    conexao.commit()
    conexao.close()

    if pratos_nomes:  # Só enviar e-mail se pelo menos um prato foi registrado
        
        cliente = buscar_cliente_por_id(cliente_id)
        if cliente:
            enviar_email_confirmacao(cliente[2], pratos_nomes, quantidades, total_pedido)
        print(f"Pedido registrado para o cliente {cliente_id} com status 'pendente'.")
    else:
        print("Nenhum prato válido foi registrado.")

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


