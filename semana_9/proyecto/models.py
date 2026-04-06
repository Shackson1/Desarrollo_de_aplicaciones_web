# models.py – Modelo SQLAlchemy
from flask_sqlalchemy import SQLAlchemy

# Nota: La instancia de 'db' normalmente se asocia con el app en app.py.
# Para evitar importaciones circulares, definimos el modelo aquí pero daremos
# vida a db en app.py.

db = SQLAlchemy()

class ProductoORM(db.Model):
    __tablename__ = 'productos'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(100), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    precio = db.Column(db.Float, nullable=False)

    # REQ-S9-01: Restricciones de integridad (opcional a nivel de BD si es SQLite viejo,
    # pero bueno tenerlo en el modelo o via CheckConstraint)
    __table_args__ = (
        db.CheckConstraint('cantidad >= 0', name='check_cantidad_positiva'),
        db.CheckConstraint('precio > 0', name='check_precio_positivo'),
    )

    def __repr__(self):
        return f'<ProductoORM {self.id}: {self.nombre}>'

    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'cantidad': self.cantidad,
            'precio': self.precio
        }
