import os

from modelos.producto import Producto
from modelos.usuario import Usuario
from servicios.archivo_servicio import ArchivoServicio


class RestauranteServicio:

    ROLES = ["Administrador", "Empleado", "Cliente"]

    def __init__(self):
        base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        self.ruta_productos = os.path.join(
            base, "datos", "productos.json"
        )
        self.ruta_usuarios = os.path.join(
            base, "datos", "usuarios.json"
        )

        self.productos = self.cargar_productos()
        self.usuarios = self.cargar_usuarios()

    # =====================================
    # USUARIOS: CARGA Y AUTENTICACIÓN
    # =====================================

    def cargar_usuarios(self):
        datos = ArchivoServicio.cargar_json(self.ruta_usuarios)
        usuarios = []

        for dato in datos:
            # Compatibilidad con usuarios creados en semanas anteriores.
            if "id" not in dato:
                dato["id"] = f"U{len(usuarios) + 1:03d}"

            if "rol" not in dato:
                dato["rol"] = "Cliente"

            usuarios.append(Usuario.from_dict(dato))

        return usuarios

    def guardar_usuarios(self):
        datos = [usuario.to_dict() for usuario in self.usuarios]
        ArchivoServicio.guardar_json(self.ruta_usuarios, datos)

    def validar_login(self, nombre_usuario, contrasena):
        for usuario in self.usuarios:
            if (
                usuario.usuario == nombre_usuario
                and usuario.contrasena == contrasena
            ):
                return usuario

        return None

    def obtener_usuarios(self):
        return self.usuarios

    def buscar_usuario(self, id_usuario):
        for usuario in self.usuarios:
            if usuario.id == str(id_usuario):
                return usuario

        return None

    def siguiente_id_usuario(self):
        numeros = []

        for usuario in self.usuarios:
            try:
                numeros.append(int(usuario.id[1:]))
            except (ValueError, IndexError):
                continue

        siguiente = max(numeros, default=0) + 1
        return f"U{siguiente:03d}"

    # =====================================
    # USUARIOS: REGISTRAR
    # =====================================

    def registrar_usuario(
        self, nombre, nombre_usuario, contrasena, rol
    ):
        nombre = nombre.strip()
        nombre_usuario = nombre_usuario.strip()
        contrasena = contrasena.strip()

        if not nombre or not nombre_usuario or not contrasena:
            return False, "Complete todos los campos."

        if rol not in self.ROLES:
            return False, "Seleccione un rol válido."

        for usuario in self.usuarios:
            if usuario.usuario.lower() == nombre_usuario.lower():
                return False, "Ese nombre de usuario ya existe."

        nuevo = Usuario(
            self.siguiente_id_usuario(),
            nombre,
            nombre_usuario,
            contrasena,
            rol
        )

        self.usuarios.append(nuevo)
        self.guardar_usuarios()

        return True, "Usuario registrado correctamente."

    # =====================================
    # USUARIOS: ACTUALIZAR
    # =====================================

    def actualizar_usuario(
        self, id_usuario, nombre, nombre_usuario, contrasena, rol
    ):
        usuario = self.buscar_usuario(id_usuario)

        if usuario is None:
            return False, "No se encontró el usuario."

        nombre = nombre.strip()
        nombre_usuario = nombre_usuario.strip()
        contrasena = contrasena.strip()

        if not nombre or not nombre_usuario:
            return False, "Nombre y usuario son obligatorios."

        if rol not in self.ROLES:
            return False, "Seleccione un rol válido."

        for otro in self.usuarios:
            if (
                otro.id != usuario.id
                and otro.usuario.lower() == nombre_usuario.lower()
            ):
                return False, "Ese nombre de usuario ya está registrado."

        usuario.nombre = nombre
        usuario.usuario = nombre_usuario
        usuario.rol = rol

        # Si la contraseña queda vacía, se conserva la anterior.
        if contrasena:
            usuario.contrasena = contrasena

        self.guardar_usuarios()
        return True, "Usuario actualizado correctamente."

    # =====================================
    # USUARIOS: ELIMINAR
    # =====================================

    def eliminar_usuario(self, id_usuario, id_administrador_actual):
        usuario = self.buscar_usuario(id_usuario)

        if usuario is None:
            return False, "No se encontró el usuario."

        if usuario.id == str(id_administrador_actual):
            return False, "No puede eliminar la cuenta administrativa activa."

        if usuario.rol == "Administrador":
            administradores = [
                u for u in self.usuarios
                if u.rol == "Administrador"
            ]

            if len(administradores) <= 1:
                return False, "Debe existir al menos un Administrador."

        self.usuarios.remove(usuario)
        self.guardar_usuarios()

        return True, "Usuario eliminado correctamente."

    # =====================================
    # PRODUCTOS: FUNCIONES DE SEMANA 15
    # =====================================

    def cargar_productos(self):
        datos = ArchivoServicio.cargar_json(self.ruta_productos)
        return [Producto.from_dict(item) for item in datos]

    def guardar_productos(self):
        datos = [producto.to_dict() for producto in self.productos]
        ArchivoServicio.guardar_json(self.ruta_productos, datos)

    def obtener_productos(self):
        return self.productos

    def buscar_producto(self, id_producto):
        for producto in self.productos:
            if producto.id == id_producto:
                return producto

        return None

    def registrar_producto(self, id_producto, nombre, precio, categoria):
        if not id_producto or not nombre or not categoria:
            return False, "Todos los campos son obligatorios."

        try:
            precio = float(precio)
        except ValueError:
            return False, "El precio debe ser numérico."

        if precio <= 0:
            return False, "El precio debe ser mayor que cero."

        if self.buscar_producto(id_producto):
            return False, "Ya existe un producto con ese ID."

        producto = Producto(id_producto, nombre, precio, categoria)
        self.productos.append(producto)
        self.guardar_productos()

        return True, "Producto registrado correctamente."

    def actualizar_producto(self, id_producto, nombre, precio, categoria):
        producto = self.buscar_producto(id_producto)

        if producto is None:
            return False, "Producto no encontrado."

        if not nombre or not categoria:
            return False, "Todos los campos son obligatorios."

        try:
            precio = float(precio)
        except ValueError:
            return False, "El precio debe ser numérico."

        if precio <= 0:
            return False, "El precio debe ser mayor que cero."

        producto.nombre = nombre
        producto.precio = precio
        producto.categoria = categoria
        self.guardar_productos()

        return True, "Producto actualizado correctamente."

    def eliminar_producto(self, id_producto):
        producto = self.buscar_producto(id_producto)

        if producto is None:
            return False, "Producto no encontrado."

        self.productos.remove(producto)
        self.guardar_productos()

        return True, "Producto eliminado correctamente."