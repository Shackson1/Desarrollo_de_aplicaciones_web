class Producto:
    def __init__(self, id, nombre, cantidad, precio):
        self._id = id
        self.nombre = nombre
        self.cantidad = cantidad
        self.precio = precio

    @property
    def id(self):
        return self._id

    def __repr__(self):
        return f"Producto(id={self.id}, nombre='{self.nombre}', cantidad={self.cantidad}, precio={self.precio})"
