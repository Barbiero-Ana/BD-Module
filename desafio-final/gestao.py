import sqlite3
from emailsender import enviar_email_confirmacao


def adicionar_prato(nome, preco):
    conexao = sqlite3.connect("restaurante.db")
    cursor = conexao.cursor()

    cursor.execute("INSERT INTO pratos (nome, preco) VALUES (?, ?)", (nome, preco))
    conexao.commit()
    conexao.close()
    print(f"Prato '{nome}' adicionado com sucesso!")

def excluir_prato(prato_id):
    conexao = sqlite3.connect("restaurante.db")
    cursor = conexao.cursor()

    cursor.execute("DELETE FROM pratos WHERE id = ?", (prato_id,))
    conexao.commit()
    conexao.close()
    print(f"Prato de ID {prato_id} excluído com sucesso!")


def listar_pratos():
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

def atualizar_prato(prato_id, novo_preco=None):
    conexao = sqlite3.connect("restaurante.db")
    cursor = conexao.cursor()

    if novo_preco:
        cursor.execute("UPDATE pratos SET preco = ? WHERE id = ?", (novo_preco, prato_id))

    conexao.commit()
    conexao.close()
    print(f"Prato de ID {prato_id} atualizado com sucesso!")

import sqlite3

def gerar_relatorio_vendas():
    conexao = sqlite3.connect("restaurante.db")
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT vp.id, c.nome, p.nome, vp.quantidade, vp.total, vp.status
        FROM vendas_pedidos vp
        JOIN clientes c ON vp.cliente_id = c.id
        JOIN pratos p ON vp.prato_id = p.id
    """)
    
    vendas = cursor.fetchall()
    conexao.close()

    if not vendas:
        print("Nenhuma venda registrada.")
        return
    
    print("\n=== RELATÓRIO DE VENDAS ===")
    for venda in vendas:
        print(f"ID Venda: {venda[0]}, Cliente: {venda[1]}, Prato: {venda[2]}, Quantidade: {venda[3]}, Total: R$ {venda[4]:.2f}, Status: {venda[5]}")




def relatorio_vendas_diarias():
    conexao = sqlite3.connect("restaurante.db")
    cursor = conexao.cursor()

    cursor.execute('''
        SELECT p.nome, SUM(vp.quantidade) AS total_vendas, SUM(vp.total) AS receita
        FROM vendas_pedidos vp
        JOIN pratos p ON vp.prato_id = p.id
        WHERE vp.status = 'entregue'
        GROUP BY p.id
    ''')

    relatorio = cursor.fetchall()
    conexao.close()

    print("\nRelatório de Vendas Diárias:")
    for item in relatorio:
        print(f"Prato: {item[0]} | Quantidade Vendida: {item[1]} | Receita: R$ {item[2]:.2f}")

def relatorio_status_pedidos():
    conexao = sqlite3.connect("restaurante.db")
    cursor = conexao.cursor()

    cursor.execute('''
        SELECT p.nome, COUNT(vp.id) AS total_pedidos, vp.status
        FROM vendas_pedidos vp
        JOIN pratos p ON vp.prato_id = p.id
        GROUP BY p.id, vp.status
    ''')

    relatorio = cursor.fetchall()
    conexao.close()

    print("\nRelatório de Status de Pedidos:")
    for item in relatorio:
        print(f"Prato: {item[0]} | Status: {item[2]} | Total de Pedidos: {item[1]}")

if __name__ == "__main__":
    while True:
        print("\n1. Adicionar Prato\n2. Excluir Prato\n3. Atualizar Prato\n4. Relatório de Vendas Diárias\n5. Relatório de Status dos Pedidos\n6. Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            nome = input("Nome do prato: ")
            preco = float(input("Preço do prato: "))
            adicionar_prato(nome, preco)
        
        elif opcao == "2":
            prato_id = int(input("ID do prato a ser excluído: "))
            excluir_prato(prato_id)

        elif opcao == "3":
            prato_id = int(input("ID do prato a ser atualizado: "))
            novo_preco = input("Novo preço (ou deixe vazio para não alterar): ")

            if novo_preco:
                novo_preco = float(novo_preco)
            atualizar_prato(prato_id, novo_preco if novo_preco else None)
        elif opcao == "4":
            relatorio_vendas_diarias()

        elif opcao == "5":
            relatorio_status_pedidos()

        elif opcao == "6":
            print("Saindo...")
            break

        else:
            print("Opção inválida!")


def listar_pedidos():
    conexao = sqlite3.connect("restaurante.db")
    cursor = conexao.cursor()
    cursor.execute("SELECT id, cliente_id, total, status FROM vendas_pedidos")
    pedidos = cursor.fetchall()
    if pedidos:
        print("\nPedidos registrados:")
        for pedido in pedidos:
            print(f"ID: {pedido[0]} | Cliente ID: {pedido[1]} | Total: R$ {pedido[2]:.2f} | Status: {pedido[3]}")
    else:
        print("Nenhum pedido registrado.")
    conexao.close()


def alterar_status_pedido():

    conexao = sqlite3.connect("restaurante.db")
    cursor = conexao.cursor()
    cursor.execute("SELECT id, cliente_id, total, status FROM vendas_pedidos")
    pedidos = cursor.fetchall()
    if pedidos:
        print("\nPedidos registrados:")
        for pedido in pedidos:
            print(f"ID: {pedido[0]} | Cliente ID: {pedido[1]} | Total: R$ {pedido[2]:.2f} | Status: {pedido[3]}")
    else:
        print("Nenhum pedido registrado.")
    conexao.close()


    pedido_id = input("\nDigite o ID do pedido para alterar o status: ")
    

    try:
        pedido_id = int(pedido_id)
    except ValueError:
        print("ID inválido, por favor insira um número.")
        return
    
    print(f"ID do pedido informado: {pedido_id}")

    conexao = sqlite3.connect("restaurante.db")
    cursor = conexao.cursor()

    # Consulta SQL 
    consulta_sql = """
        SELECT vp.id, c.nome, c.email, p.nome, vp.quantidade, vp.total, vp.status
        FROM vendas_pedidos vp
        JOIN clientes c ON vp.cliente_id = c.id
        JOIN pratos p ON vp.prato_id = p.id
        WHERE vp.id = ?
    """
    cursor.execute(consulta_sql, (pedido_id,))
    resultado = cursor.fetchone()
    
    if not resultado:
        print(f"Pedido com ID {pedido_id} não encontrado.")
        # depuracao pra achar o maldito ERRO
        cursor.execute("SELECT id, cliente_id, prato_id, quantidade, total, status FROM vendas_pedidos WHERE id = ?", (pedido_id,))
        pedido = cursor.fetchone()
        if pedido:
            print(f"Pedido encontrado diretamente: {pedido}")
            cursor.execute("SELECT id, nome FROM clientes WHERE id = ?", (pedido[1],))
            print(f"Cliente: {cursor.fetchone()}")
            cursor.execute("SELECT id, nome FROM pratos WHERE id = ?", (pedido[2],))
            print(f"Prato: {cursor.fetchone()}")
        else:
            print("Pedido não existe na tabela vendas_pedidos.")
        conexao.close()
        return


    id_pedido, nome_cliente, email_cliente, nome_prato, quantidade, total, status = resultado
    print(f"Pedido encontrado: {nome_cliente} pediu {quantidade} de {nome_prato} (Status atual: {status})")

    novo_status = input("Digite o novo status (pendente, preparando, pronto, entregue): ")

    # NOVO STATUS
    if novo_status not in ['pendente', 'preparando', 'pronto', 'entregue']:
        print("Status inválido. Use um dos seguintes: 'pendente', 'preparando', 'pronto', 'entregue'.")
        conexao.close()
        return
    
    # att o status do pedido
    cursor.execute("""
        UPDATE vendas_pedidos
        SET status = ?
        WHERE id = ?
    """, (novo_status, pedido_id))
    
    if cursor.rowcount == 0:
        print(f"Erro: Nenhum pedido com ID {pedido_id} foi atualizado.")
    else:
        conexao.commit()
        try:
            enviar_email_confirmacao(email_cliente, [nome_prato], [quantidade], total)
            print(f"Status do pedido {pedido_id} alterado para '{novo_status}' com sucesso!")
        except Exception as e:
            print(f"Status alterado, mas falha ao enviar e-mail: {e}")
    
    conexao.close()