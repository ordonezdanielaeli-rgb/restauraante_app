import tkinter as tk
from tkinter import ttk, messagebox


class LoginView:

    def __init__(self, root, servicio, abrir_main):
        self.root = root
        self.servicio = servicio
        self.abrir_main = abrir_main

        self.root.title("Restaurante App - Inicio de sesión")
        self.root.geometry("450x350")
        self.root.resizable(False, False)

        self.crear_interfaz()

    def crear_interfaz(self):
        contenedor = ttk.Frame(self.root, padding=30)
        contenedor.pack(expand=True)

        ttk.Label(
            contenedor,
            text="RESTAURANTE APP",
            font=("Arial", 20, "bold")
        ).pack(pady=15)

        ttk.Label(
            contenedor,
            text="Inicio de sesión"
        ).pack(pady=5)

        ttk.Label(contenedor, text="Usuario:").pack(anchor="w", pady=(15, 5))

        self.entrada_usuario = ttk.Entry(contenedor, width=35)
        self.entrada_usuario.pack()

        ttk.Label(contenedor, text="Contraseña:").pack(
            anchor="w", pady=(15, 5)
        )

        self.entrada_contrasena = ttk.Entry(
            contenedor, width=35, show="*"
        )
        self.entrada_contrasena.pack()

        ttk.Button(
            contenedor,
            text="Ingresar",
            command=self.iniciar_sesion
        ).pack(pady=25)

        self.entrada_contrasena.bind(
            "<Return>",
            self.evento_enter_login
        )

    def evento_enter_login(self, event):
        self.iniciar_sesion()

    def iniciar_sesion(self):
        nombre_usuario = self.entrada_usuario.get().strip()
        contrasena = self.entrada_contrasena.get().strip()

        usuario = self.servicio.validar_login(
            nombre_usuario,
            contrasena
        )

        if usuario:
            self.abrir_main(usuario)
        else:
            messagebox.showerror(
                "Acceso denegado",
                "Usuario o contraseña incorrectos."
            )