import sqlite3
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Função para buscar o cliente pelo ID no banco de dados
def buscar_cliente_por_id(cliente_id):
    conexao = sqlite3.connect("restaurante.db")
    cursor = conexao.cursor()

    # Consultando o banco para obter os dados do cliente
    cursor.execute("SELECT * FROM clientes WHERE id = ?", (cliente_id,))
    cliente = cursor.fetchone()

    conexao.close()

    return cliente  # Retorna o cliente ou None se não encontrar

# Função para registrar um pedido
def registrar_pedido(cliente_id, pratos, quantidade):
    conexao = sqlite3.connect("restaurante.db")
    cursor = conexao.cursor()

    # Calculando o valor total do pedido
    total = 0
    for prato_id, qtd in zip(pratos, quantidade):
        cursor.execute("SELECT preco FROM pratos WHERE id = ?", (prato_id,))
        preco = cursor.fetchone()[0]
        total += preco * qtd
    
    # Inserindo pedido na tabela 'vendas_pedidos'
    cursor.execute('''
        INSERT INTO vendas_pedidos (cliente_id, prato_id, quantidade, total, status)
        VALUES (?, ?, ?, ?, 'confirmado')
    ''', (cliente_id, pratos[0], quantidade[0], total))  # Apenas exemplo para 1 prato

    conexao.commit()
    conexao.close()

    # Buscar o e-mail do cliente
    cliente = buscar_cliente_por_id(cliente_id)
    if cliente:
        # Enviar e-mail de confirmação
        enviar_email_confirmacao(cliente[2], pratos, quantidade, total)
        print(f"Pedido registrado para o cliente {cliente[1]} e e-mail de confirmação enviado!")

# Função para enviar e-mail de confirmação
def enviar_email_confirmacao(email_cliente, pratos, quantidade, total):
    # Configurações de envio de e-mail
    email_remetente = "seuemail@dominio.com"
    senha_remetente = "sua_senha"
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
    
    for p, q in zip(pratos, quantidade):
        corpo_email += f"Prato ID: {p} | Quantidade: {q}\n"
    
    corpo_email += f"\nTotal: R$ {total:.2f}\n\nAguarde a confirmação do status de entrega.\n\nObrigado por escolher nosso restaurante!"

    mensagem.attach(MIMEText(corpo_email, 'plain'))

    try:
        # Estabelecendo a conexão com o servidor SMTP
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(email_remetente, senha_remetente)

        # Enviando o e-mail
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
