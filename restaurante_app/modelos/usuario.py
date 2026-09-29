class Usuario:
    def __init__(self, id, nombre, usuario, contrasena, rol):
        self.id = str(id)
        self.nombre = nombre
        self.usuario = usuario
        self.contrasena = contrasena
        self.rol = rol

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "usuario": self.usuario,
            "contrasena": self.contrasena,
            "rol": self.rol
        }

    @staticmethod
    def from_dict(data):
        return Usuario(
            data["id"],
            data["nombre"],
            data["usuario"],
            data.get("contrasena", ""),
            data.get("rol", "Cliente")
        )