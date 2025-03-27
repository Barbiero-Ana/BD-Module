import sqlite3

def criar_banco():
    conexao = sqlite3.connect("restaurante.db")
    cursor = conexao.cursor()

    # Tabela de usuários (gestor e atendente)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            cargo TEXT CHECK (cargo IN ('gestor', 'atendente')) NOT NULL,
            email TEXT UNIQUE NOT NULL,
            senha TEXT NOT NULL
        )
    ''')

    # Tabela de pratos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pratos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            preco REAL NOT NULL
        )
    ''')

    # Tabela de clientes
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL
        )
    ''')

    # Tabela de vendas/pedidos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS vendas_pedidos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente_id INTEGER,
            prato_id INTEGER,
            quantidade INTEGER NOT NULL,
            total REAL NOT NULL,
            status TEXT CHECK (status IN ('pendente', 'preparando', 'pronto', 'entregue')) DEFAULT 'pendente',
            FOREIGN KEY(cliente_id) REFERENCES clientes(id),
            FOREIGN KEY(prato_id) REFERENCES pratos(id)
        )
    ''')

    # Tabela de cupons de desconto
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cupons (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            codigo TEXT UNIQUE NOT NULL,
            desconto REAL NOT NULL,
            cliente_id INTEGER,
            FOREIGN KEY(cliente_id) REFERENCES clientes(id)
        )
    ''')

    conexao.commit()
    conexao.close()

if __name__ == "__main__":
    criar_banco()
    print("Banco de dados criado com sucesso!")
