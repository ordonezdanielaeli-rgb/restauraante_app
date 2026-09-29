import os
import tkinter as tk
from tkinter import ttk, messagebox


class MainView:

    def __init__(self, root, servicio, usuario_actual, cerrar_sesion):
        self.root = root
        self.servicio = servicio
        self.usuario_actual = usuario_actual
        self.cerrar_sesion = cerrar_sesion
        self.usuario_seleccionado_id = None

        self.root.title("Restaurante App")
        self.root.geometry("1000x700")
        self.root.minsize(850, 600)

        self.crear_interfaz()

    # ==========================================
    # VENTANA Y NAVEGACIÓN
    # ==========================================

    def crear_interfaz(self):
        encabezado = ttk.Frame(self.root, padding=12)
        encabezado.pack(fill="x")

        # Logo de la aplicación
        # Se agregará después de colocar un archivo de imagen válido.

        ttk.Label(
            encabezado,
            text="RESTAURANTE APP",
            font=("Arial", 20, "bold")
        ).pack(side="left")

        nombre_rol = (
            f"{self.usuario_actual.nombre} "
            f"({self.usuario_actual.rol})"
        )

        ttk.Label(
            encabezado,
            text=nombre_rol
        ).pack(side="left", padx=25)

        ttk.Button(
            encabezado,
            text="Cerrar sesión",
            command=self.cerrar_sesion
        ).pack(side="right")

        # Contenedor de las pestañas
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(
            fill="both",
            expand=True,
            padx=12,
            pady=10
        )

        # Pestaña de productos
        self.tab_productos = ttk.Frame(self.notebook, padding=12)
        self.notebook.add(self.tab_productos, text="Productos")
        self.crear_tab_productos()

        # La pestaña de usuarios solo aparece para administradores
        if self.usuario_actual.rol == "Administrador":
            self.tab_usuarios = ttk.Frame(self.notebook, padding=12)
            self.notebook.add(self.tab_usuarios, text="Usuarios")
            self.crear_tab_usuarios()

    # ==========================================
    # PRODUCTOS
    # ==========================================

    def crear_tab_productos(self):
        ttk.Label(
            self.tab_productos,
            text="Gestión de productos",
            font=("Arial", 17, "bold")
        ).pack(anchor="w", pady=(0, 10))

        formulario = ttk.LabelFrame(
            self.tab_productos,
            text="Datos del producto",
            padding=12
        )
        formulario.pack(fill="x")

        ttk.Label(formulario, text="ID:").grid(row=0, column=0, padx=5, pady=5)
        self.prod_id = ttk.Entry(formulario, width=22)
        self.prod_id.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(formulario, text="Nombre:").grid(row=0, column=2, padx=5, pady=5)
        self.prod_nombre = ttk.Entry(formulario, width=25)
        self.prod_nombre.grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(formulario, text="Precio:").grid(row=1, column=0, padx=5, pady=5)
        self.prod_precio = ttk.Entry(formulario, width=22)
        self.prod_precio.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(formulario, text="Categoría:").grid(row=1, column=2, padx=5, pady=5)
        self.prod_categoria = ttk.Entry(formulario, width=25)
        self.prod_categoria.grid(row=1, column=3, padx=5, pady=5)

        botones = ttk.Frame(self.tab_productos, padding=8)
        botones.pack(fill="x")

        ttk.Button(
            botones, text="Registrar",
            command=self.registrar_producto
        ).pack(side="left", padx=4)

        ttk.Button(
            botones, text="Cargar / Consultar",
            command=self.cargar_producto
        ).pack(side="left", padx=4)

        ttk.Button(
            botones, text="Actualizar",
            command=self.actualizar_producto
        ).pack(side="left", padx=4)

        ttk.Button(
            botones, text="Eliminar",
            command=self.eliminar_producto
        ).pack(side="left", padx=4)

        ttk.Button(
            botones, text="Limpiar",
            command=self.limpiar_producto
        ).pack(side="left", padx=4)

        tabla_frame = ttk.LabelFrame(
            self.tab_productos,
            text="Productos registrados",
            padding=8
        )
        tabla_frame.pack(fill="both", expand=True, pady=8)

        columnas = ("id", "nombre", "precio", "categoria")
        self.tabla_productos = ttk.Treeview(
            tabla_frame,
            columns=columnas,
            show="headings",
            height=12
        )

        encabezados = {
            "id": "ID",
            "nombre": "Nombre",
            "precio": "Precio",
            "categoria": "Categoría"
        }

        for columna, texto in encabezados.items():
            self.tabla_productos.heading(columna, text=texto)
            self.tabla_productos.column(columna, width=180)

        self.tabla_productos.pack(fill="both", expand=True)
        self.actualizar_tabla_productos()

    def registrar_producto(self):
        ok, mensaje = self.servicio.registrar_producto(
            self.prod_id.get().strip(),
            self.prod_nombre.get().strip(),
            self.prod_precio.get().strip(),
            self.prod_categoria.get().strip()
        )

        if ok:
            messagebox.showinfo("Correcto", mensaje)
            self.actualizar_tabla_productos()
            self.limpiar_producto()
        else:
            messagebox.showerror("Revisar datos", mensaje)

    def cargar_producto(self):
        producto = self.servicio.buscar_producto(
            self.prod_id.get().strip()
        )

        if producto is None:
            messagebox.showerror("No encontrado", "No existe ese producto.")
            return

        self.prod_nombre.delete(0, tk.END)
        self.prod_nombre.insert(0, producto.nombre)

        self.prod_precio.delete(0, tk.END)
        self.prod_precio.insert(0, str(producto.precio))

        self.prod_categoria.delete(0, tk.END)
        self.prod_categoria.insert(0, producto.categoria)

    def actualizar_producto(self):
        ok, mensaje = self.servicio.actualizar_producto(
            self.prod_id.get().strip(),
            self.prod_nombre.get().strip(),
            self.prod_precio.get().strip(),
            self.prod_categoria.get().strip()
        )

        if ok:
            messagebox.showinfo("Correcto", mensaje)
            self.actualizar_tabla_productos()
            self.limpiar_producto()
        else:
            messagebox.showerror("Revisar datos", mensaje)

    def eliminar_producto(self):
        id_producto = self.prod_id.get().strip()

        if not id_producto:
            messagebox.showwarning("Aviso", "Ingrese el ID del producto.")
            return

        confirmar = messagebox.askyesno(
            "Confirmar",
            "¿Desea eliminar este producto?"
        )

        if confirmar:
            ok, mensaje = self.servicio.eliminar_producto(id_producto)

            if ok:
                messagebox.showinfo("Correcto", mensaje)
                self.actualizar_tabla_productos()
                self.limpiar_producto()
            else:
                messagebox.showerror("Error", mensaje)

    def limpiar_producto(self):
        for entrada in (
            self.prod_id,
            self.prod_nombre,
            self.prod_precio,
            self.prod_categoria
        ):
            entrada.delete(0, tk.END)

    def actualizar_tabla_productos(self):
        for item in self.tabla_productos.get_children():
            self.tabla_productos.delete(item)

        for producto in self.servicio.obtener_productos():
            self.tabla_productos.insert(
                "",
                tk.END,
                values=(
                    producto.id,
                    producto.nombre,
                    f"{producto.precio:.2f}",
                    producto.categoria
                )
            )

    # ==========================================
    # USUARIOS: INTERFAZ
    # ==========================================

    def crear_tab_usuarios(self):
        ttk.Label(
            self.tab_usuarios,
            text="Administración de usuarios",
            font=("Arial", 17, "bold")
        ).pack(anchor="w", pady=(0, 10))

        formulario = ttk.LabelFrame(
            self.tab_usuarios,
            text="Formulario de usuario",
            padding=12
        )
        formulario.pack(fill="x")

        ttk.Label(formulario, text="ID:").grid(row=0, column=0, padx=5, pady=5)
        self.usr_id = ttk.Entry(formulario, width=22, state="readonly")
        self.usr_id.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(formulario, text="Nombre:").grid(row=0, column=2, padx=5, pady=5)
        self.usr_nombre = ttk.Entry(formulario, width=25)
        self.usr_nombre.grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(formulario, text="Usuario:").grid(row=1, column=0, padx=5, pady=5)
        self.usr_usuario = ttk.Entry(formulario, width=22)
        self.usr_usuario.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(formulario, text="Contraseña:").grid(row=1, column=2, padx=5, pady=5)
        self.usr_contrasena = ttk.Entry(formulario, width=25, show="*")
        self.usr_contrasena.grid(row=1, column=3, padx=5, pady=5)

        ttk.Label(formulario, text="Rol:").grid(row=2, column=0, padx=5, pady=5)
        self.usr_rol = ttk.Combobox(
            formulario,
            values=["Administrador", "Empleado", "Cliente"],
            state="readonly",
            width=19
        )
        self.usr_rol.grid(row=2, column=1, padx=5, pady=5)
        self.usr_rol.set("Cliente")

        self.etiqueta_rol = ttk.Label(
            formulario,
            text="Seleccione el rol del usuario."
        )
        self.etiqueta_rol.grid(
            row=2, column=2, columnspan=2, padx=5, pady=5, sticky="w"
        )

        # Evento virtual del Combobox.
        self.usr_rol.bind(
            "<<ComboboxSelected>>",
            self.evento_cambio_rol
        )

        botones = ttk.Frame(self.tab_usuarios, padding=8)
        botones.pack(fill="x")

        ttk.Button(
            botones, text="Registrar",
            command=self.registrar_usuario
        ).pack(side="left", padx=4)

        ttk.Button(
            botones, text="Actualizar",
            command=self.actualizar_usuario
        ).pack(side="left", padx=4)

        ttk.Button(
            botones, text="Eliminar",
            command=self.eliminar_usuario
        ).pack(side="left", padx=4)

        ttk.Button(
            botones, text="Limpiar",
            command=self.limpiar_usuario
        ).pack(side="left", padx=4)

        ttk.Label(
            self.tab_usuarios,
            text="Seleccione una fila para cargar sus datos. "
                 "Enter registra y Escape limpia el formulario.",
            foreground="gray"
        ).pack(anchor="w", pady=4)

        tabla_frame = ttk.LabelFrame(
            self.tab_usuarios,
            text="Usuarios registrados",
            padding=8
        )
        tabla_frame.pack(fill="both", expand=True, pady=8)

        columnas = ("id", "nombre", "usuario", "rol")
        self.tabla_usuarios = ttk.Treeview(
            tabla_frame,
            columns=columnas,
            show="headings",
            height=10
        )

        for columna, texto in {
            "id": "Identificador",
            "nombre": "Nombre",
            "usuario": "Usuario",
            "rol": "Rol"
        }.items():
            self.tabla_usuarios.heading(columna, text=texto)
            self.tabla_usuarios.column(columna, width=180)

        self.tabla_usuarios.pack(fill="both", expand=True)

        # Evento de selección de fila.
        self.tabla_usuarios.bind(
            "<<TreeviewSelect>>",
            self.evento_seleccionar_usuario
        )

        # Atajos de teclado para el formulario.
        self.tab_usuarios.bind(
            "<Return>",
            self.evento_enter_usuario
        )
        self.tab_usuarios.bind(
            "<Escape>",
            self.evento_escape_usuario
        )

        # Permite que los atajos funcionen mientras se escribe
        # en los campos del formulario.
        for widget in (
            self.usr_nombre,
            self.usr_usuario,
            self.usr_contrasena,
            self.usr_rol
        ):
            widget.bind("<Return>", self.evento_enter_usuario)
            widget.bind("<Escape>", self.evento_escape_usuario)

        self.actualizar_tabla_usuarios()

    # ==========================================
    # USUARIOS: EVENTOS
    # ==========================================

    def evento_seleccionar_usuario(self, event):
        seleccion = self.tabla_usuarios.selection()

        if not seleccion:
            return

        valores = self.tabla_usuarios.item(
            seleccion[0],
            "values"
        )

        if not valores:
            return

        id_usuario = valores[0]

        # Se consulta el objeto mediante el servicio.
        usuario = self.servicio.buscar_usuario(id_usuario)

        if usuario is None:
            return

        self.usuario_seleccionado_id = usuario.id

        self.usr_id.configure(state="normal")
        self.usr_id.delete(0, tk.END)
        self.usr_id.insert(0, usuario.id)
        self.usr_id.configure(state="readonly")

        self.usr_nombre.delete(0, tk.END)
        self.usr_nombre.insert(0, usuario.nombre)

        self.usr_usuario.delete(0, tk.END)
        self.usr_usuario.insert(0, usuario.usuario)

        # No se carga la contraseña en el formulario ni en el Treeview.
        self.usr_contrasena.delete(0, tk.END)

        self.usr_rol.set(usuario.rol)
        self.etiqueta_rol.config(text=f"Rol seleccionado: {usuario.rol}")

    def evento_enter_usuario(self, event):
        # Reutiliza el método ya existente; no duplica su lógica.
        self.registrar_usuario()
        return "break"

    def evento_escape_usuario(self, event):
        self.limpiar_usuario()
        return "break"

    def evento_cambio_rol(self, event):
        rol = self.usr_rol.get()
        self.etiqueta_rol.config(
            text=f"Rol seleccionado: {rol}"
        )

    # ==========================================
    # USUARIOS: OPERACIONES
    # ==========================================

    def registrar_usuario(self):
        ok, mensaje = self.servicio.registrar_usuario(
            self.usr_nombre.get(),
            self.usr_usuario.get(),
            self.usr_contrasena.get(),
            self.usr_rol.get()
        )

        if ok:
            messagebox.showinfo("Correcto", mensaje)
            self.actualizar_tabla_usuarios()
            self.limpiar_usuario()
        else:
            messagebox.showerror("Revisar datos", mensaje)

    def actualizar_usuario(self):
        id_usuario = self.usuario_seleccionado_id

        if not id_usuario:
            messagebox.showwarning(
                "Seleccione usuario",
                "Seleccione primero una fila del Treeview."
            )
            return

        ok, mensaje = self.servicio.actualizar_usuario(
            id_usuario,
            self.usr_nombre.get(),
            self.usr_usuario.get(),
            self.usr_contrasena.get(),
            self.usr_rol.get()
        )

        if ok:
            messagebox.showinfo("Correcto", mensaje)
            self.actualizar_tabla_usuarios()
            self.limpiar_usuario()
        else:
            messagebox.showerror("Revisar datos", mensaje)

    def eliminar_usuario(self):
        id_usuario = self.usuario_seleccionado_id

        if not id_usuario:
            messagebox.showwarning(
                "Seleccione usuario",
                "Seleccione primero una fila del Treeview."
            )
            return

        confirmar = messagebox.askyesno(
            "Confirmar eliminación",
            "¿Está seguro de eliminar este usuario?"
        )

        if not confirmar:
            return

        ok, mensaje = self.servicio.eliminar_usuario(
            id_usuario,
            self.usuario_actual.id
        )

        if ok:
            messagebox.showinfo("Correcto", mensaje)
            self.actualizar_tabla_usuarios()
            self.limpiar_usuario()
        else:
            messagebox.showerror("No se pudo eliminar", mensaje)

    def limpiar_usuario(self):
        self.usuario_seleccionado_id = None

        self.usr_id.configure(state="normal")
        self.usr_id.delete(0, tk.END)
        self.usr_id.configure(state="readonly")

        self.usr_nombre.delete(0, tk.END)
        self.usr_usuario.delete(0, tk.END)
        self.usr_contrasena.delete(0, tk.END)
        self.usr_rol.set("Cliente")

        self.etiqueta_rol.config(
            text="Seleccione el rol del usuario."
        )

        seleccion = self.tabla_usuarios.selection()
        if seleccion:
            self.tabla_usuarios.selection_remove(seleccion)

    def actualizar_tabla_usuarios(self):
        for item in self.tabla_usuarios.get_children():
            self.tabla_usuarios.delete(item)

        for usuario in self.servicio.obtener_usuarios():
            self.tabla_usuarios.insert(
                "",
                tk.END,
                values=(
                    usuario.id,
                    usuario.nombre,
                    usuario.usuario,
                    usuario.rol
                )
            )