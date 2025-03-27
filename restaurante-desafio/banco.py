import sqlite3

def inicializar_bd():
    conn = sqlite3.connect("restaurante.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id TEXT UNIQUE,
            email TEXT UNIQUE
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cupons_enviados (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER,
            email TEXT UNIQUE,
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
        )
    """)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    inicializar_bd()
    print("Banco de dados inicializado!")
