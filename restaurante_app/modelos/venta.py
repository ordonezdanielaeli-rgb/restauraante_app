class Venta:
    def __init__(self, id, producto_id, cantidad, total):
        self.id = id
        self.producto_id = producto_id
        self.cantidad = cantidad
        self.total = total

    def to_dict(self):
        return {
            "id": self.id,
            "producto_id": self.producto_id,
            "cantidad": self.cantidad,
            "total": self.total
        }