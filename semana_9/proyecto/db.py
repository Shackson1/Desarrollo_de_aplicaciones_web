import sqlite3
import os
from models import db

DATABASE = 'inventario.db'

def get_db_connection():
    """Conexión para SQLite raw (Semanas anteriores)"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Inicialización manual de tablas SQLite raw"""
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
        conn.commit()
        conn.close()
        print("Base de datos SQLite raw inicializada.")

def configure_sqlalchemy(app):
    """Configuración de SQLAlchemy ORM (Semana 12)"""
    # Usamos la ruta absoluta para evitar problemas con la carpeta instance/
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, DATABASE)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    
    with app.app_context():
        # Crea las tablas si no existen (sin borrar datos)
        db.create_all()
        print("SQLAlchemy ORM sincronizado con inventario.db.")
