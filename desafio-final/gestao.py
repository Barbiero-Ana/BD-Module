import sqlite3

# Funções de gerenciamento de pratos
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

def atualizar_prato(prato_id, novo_nome=None, novo_preco=None):
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








# Funções de relatório de vendas
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
            novo_nome = input("Novo nome (ou deixe vazio para não alterar): ")
            novo_preco = input("Novo preço (ou deixe vazio para não alterar): ")

            if novo_preco:
                novo_preco = float(novo_preco)
            atualizar_prato(prato_id, novo_nome if novo_nome else None, novo_preco if novo_preco else None)

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
    listar_pedidos()
    pedido_id = int(input("\nDigite o ID do pedido para alterar o status: "))
    novo_status = input("Digite o novo status do pedido (pendente, pronto, entregue, em atraso): ").lower()
    
    if novo_status not in ['pendente', 'pronto', 'entregue', 'em atraso']:
        print("Status inválido! Os valores válidos são: 'pendente', 'pronto', 'entregue', 'em atraso'.")
        return
    
    conexao = sqlite3.connect("restaurante.db")
    cursor = conexao.cursor()
    
    cursor.execute("UPDATE vendas_pedidos SET status = ? WHERE id = ?", (novo_status, pedido_id))
    
    if cursor.rowcount > 0:
        conexao.commit()
        print(f"Status do pedido {pedido_id} alterado para '{novo_status}'.")
    else:
        print("Pedido não encontrado.")
    
    conexao.close()
