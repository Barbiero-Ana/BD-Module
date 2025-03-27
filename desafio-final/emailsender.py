import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Função para enviar um e-mail
def enviar_email(remetente, senha, destinatario, assunto, corpo):
    try:
        # Configurações do servidor SMTP
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        
        # Criando a mensagem
        mensagem = MIMEMultipart()
        mensagem['From'] = remetente
        mensagem['To'] = destinatario
        mensagem['Subject'] = assunto
        mensagem.attach(MIMEText(corpo, 'plain'))

        # Estabelecendo a conexão com o servidor SMTP
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(remetente, senha)

        # Enviando o e-mail
        server.sendmail(remetente, destinatario, mensagem.as_string())
        server.quit()
        print("E-mail enviado com sucesso!")
    except Exception as e:
        print(f"Erro ao enviar o e-mail: {e}")

# Função específica para enviar e-mail de confirmação de pedido
def enviar_email_confirmacao(email_cliente, pratos, quantidade, total):
    # Configurações de envio de e-mail
    email_remetente = "seuemail@dominio.com"
    senha_remetente = "sua_senha"
    
    assunto = "Confirmação de Pedido"
    corpo = f"""
    Olá, seu pedido foi confirmado! Detalhes do pedido:

    Pratos solicitados:
    """
    
    for p, q in zip(pratos, quantidade):
        corpo += f"Prato ID: {p} | Quantidade: {q}\n"
    
    corpo += f"\nTotal: R$ {total:.2f}\n\nAguarde a confirmação do status de entrega.\n\nObrigado por escolher nosso restaurante!"

    # Enviar o e-mail de confirmação
    enviar_email(email_remetente, senha_remetente, email_cliente, assunto, corpo)

# Função para enviar cupom de desconto
def enviar_email_cupom(email_cliente, cupom_codigo):
    # Configurações de envio de e-mail
    email_remetente = "seuemail@dominio.com"
    senha_remetente = "sua_senha"
    
    assunto = "Cupom de Desconto Exclusivo"
    corpo = f"""
    Olá!

    Aqui está o seu cupom de desconto exclusivo: {cupom_codigo}

    Utilize-o em sua próxima compra. Aproveite e bom apetite!

    Atenciosamente,
    Restaurante X
    """
    
    # Enviar o e-mail com o cupom
    enviar_email(email_remetente, senha_remetente, email_cliente, assunto, corpo)
