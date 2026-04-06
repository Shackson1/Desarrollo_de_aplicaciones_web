import sqlite3
import os

DATABASE = 'inventario.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    if not os.path.exists(DATABASE):
        conn = get_db_connection()
        # Tabla de productos
        conn.execute('''
            CREATE TABLE IF NOT EXISTS productos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                cantidad INTEGER NOT NULL,
                precio REAL NOT NULL
            )
        ''')
        # Podemos añadir otras tablas aquí (ej. clientes) si el usuario lo requiere en el futuro
        conn.commit()
        conn.close()
        print("Base de datos inicializada correctamente.")

if __name__ == '__main__':
    init_db()
