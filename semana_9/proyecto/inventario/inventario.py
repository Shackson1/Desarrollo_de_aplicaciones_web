import os
import json
import csv
from .bd import get_db_connection
from .productos import Producto

# Ruta base hacia la carpeta data/
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')

def _ruta(nombre_archivo):
    """Devuelve la ruta absoluta de un archivo dentro de data/"""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR, exist_ok=True)
    return os.path.join(DATA_DIR, nombre_archivo)

class Inventario:
    def __init__(self):
        # Colección: Diccionario para búsqueda rápida por ID
        self.productos = {}

    def cargar_desde_db(self):
        """Llena el diccionario leyendo la tabla productos de SQLite."""
        self.productos = {}
        conn = get_db_connection()
        rows = conn.execute('SELECT * FROM productos').fetchall()
        for row in rows:
            p = Producto(row['id'], row['nombre'], row['cantidad'], row['precio'])
            self.productos[p.id] = p
        conn.close()

    def agregar_producto(self, nombre, cantidad, precio):
        """Añade un nuevo producto a la DB y actualiza el diccionario."""
        conn = get_db_connection()
        cursor = conn.execute(
            'INSERT INTO productos (nombre, cantidad, precio) VALUES (?, ?, ?)',
            (nombre, cantidad, precio)
        )
        new_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        # Actualizar colección en memoria
        nuevo_p = Producto(new_id, nombre, cantidad, precio)
        self.productos[new_id] = nuevo_p
        return nuevo_p

    def eliminar_producto(self, producto_id):
        """Elimina un producto por ID de la DB y del diccionario."""
        if producto_id in self.productos:
            conn = get_db_connection()
            conn.execute('DELETE FROM productos WHERE id = ?', (producto_id,))
            conn.commit()
            conn.close()
            del self.productos[producto_id]
            return True
        return False

    def actualizar_producto(self, producto_id, nueva_cantidad=None, nuevo_precio=None):
        """Actualiza cantidad o precio de un producto por ID."""
        if producto_id in self.productos:
            p = self.productos[producto_id]
            
            # Determinar nuevos valores
            cantidad = nueva_cantidad if nueva_cantidad is not None else p.cantidad
            precio = nuevo_precio if nuevo_precio is not None else p.precio
            
            conn = get_db_connection()
            conn.execute(
                'UPDATE productos SET cantidad = ?, precio = ? WHERE id = ?',
                (cantidad, precio, producto_id)
            )
            conn.commit()
            conn.close()
            
            # Actualizar en memoria
            p.cantidad = cantidad
            p.precio = precio
            return True
        return False

    def buscar_por_nombre(self, nombre):
        """Busca productos por nombre (usando listas para devolver resultados)."""
        resultados = [p for p in self.productos.values() if nombre.lower() in p.nombre.lower()]
        return resultados

    def listar_todos(self):
        """Devuelve una lista con todos los productos del inventario."""
        return list(self.productos.values())

    def obtener_por_id(self, producto_id):
        """Devuelve un producto por su ID usando el diccionario."""
        return self.productos.get(producto_id)

    # REQUERIMIENTOS SEMANA 12: MÉTODOS EXPORTAR/IMPORTAR
    def guardar_txt(self):
        """Sincroniza el inventario actual con el archivo TXT."""
        try:
            with open(_ruta('datos.txt'), 'w', encoding='utf-8') as f:
                for p in self.productos.values():
                    f.write(f"{p.id}|{p.nombre}|{p.cantidad}|{p.precio}\n")
            return True
        except (IOError, PermissionError) as e:
            print(f"Error al guardar TXT: {e}")
            return False

    def leer_txt(self):
        """Lee el archivo TXT y devuelve una lista de diccionarios."""
        try:
            ruta = _ruta('datos.txt')
            if not os.path.exists(ruta): return []
            productos = []
            with open(ruta, 'r', encoding='utf-8') as f:
                for line in f:
                    parts = line.strip().split('|')
                    if len(parts) == 4:
                        productos.append({
                            'id': int(parts[0]), 'nombre': parts[1],
                            'cantidad': int(parts[2]), 'precio': float(parts[3])
                        })
            return productos
        except Exception: return []

    def guardar_csv(self):
        """Sincroniza el inventario actual con el archivo CSV."""
        try:
            with open(_ruta('datos.csv'), 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['id', 'nombre', 'cantidad', 'precio'])
                for p in self.productos.values():
                    writer.writerow([p.id, p.nombre, p.cantidad, p.precio])
            return True
        except Exception: return False

    def leer_csv(self):
        """Lee el archivo CSV y devuelve una lista de diccionarios."""
        try:
            ruta = _ruta('datos.csv')
            if not os.path.exists(ruta): return []
            with open(ruta, 'r', encoding='utf-8') as f:
                return list(csv.DictReader(f))
        except Exception: return []

    def guardar_json(self):
        """Sincroniza el inventario actual con el archivo JSON."""
        try:
            data = [
                {'id': p.id, 'nombre': p.nombre, 'cantidad': p.cantidad, 'precio': float(p.precio)}
                for p in self.productos.values()
            ]
            with open(_ruta('datos.json'), 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            return True
        except Exception: return False

    def leer_json(self):
        """Lee el archivo JSON y devuelve una lista de diccionarios."""
        try:
            ruta = _ruta('datos.json')
            if not os.path.exists(ruta): return []
            with open(ruta, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception: return []
