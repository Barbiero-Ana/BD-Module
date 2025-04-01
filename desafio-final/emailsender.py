import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os

load_dotenv()

user_email = os.getenv('USER_EMAIL')
user_password = os.getenv('USER_PASSWORD')

def enviar_email(remetente, senha, destinatario, assunto, corpo):
    try:
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        
        mensagem = MIMEMultipart()
        mensagem['From'] = remetente
        mensagem['To'] = destinatario
        mensagem['Subject'] = assunto
        mensagem.attach(MIMEText(corpo, 'plain'))

        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(remetente, senha)
        server.sendmail(remetente, destinatario, mensagem.as_string())
        server.quit()
        print("E-mail enviado com sucesso!")
    except Exception as e:
        print(f"Erro ao enviar o e-mail: {e}")

def enviar_email_confirmacao(email_cliente, pratos, quantidade, total):
    email_remetente = user_email
    senha_remetente = user_password
    
    assunto = "Confirmação de Pedido"
    corpo = f"""
    Olá, seu pedido foi confirmado! Detalhes do pedido:

    Pratos solicitados:
    """
    
    for p, q in zip(pratos, quantidade):
        corpo += f"Prato ID: {p} | Quantidade: {q}\n"
    
    corpo += f"\nTotal: R$ {total:.2f}\n\nAguarde a confirmação do status de entrega.\n\nObrigado por escolher nosso restaurante!"

    enviar_email(email_remetente, senha_remetente, email_cliente, assunto, corpo)

def enviar_email_cupom(email_cliente, cupom_codigo):
    email_remetente = user_email
    senha_remetente = user_password
    
    assunto = "Cupom de Desconto Exclusivo"
    corpo = f"""
    Olá!

    Aqui está o seu cupom de desconto exclusivo: {cupom_codigo}

    Utilize-o em sua próxima compra. Aproveite e bom apetite!

    Atenciosamente,
    Restaurante Cyber
    """
    
    enviar_email(email_remetente, senha_remetente, email_cliente, assunto, corpo)
