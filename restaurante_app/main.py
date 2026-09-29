import tkinter as tk

from servicios.restaurante_servicio import RestauranteServicio
from ui.login_view import LoginView
from ui.main_view import MainView


class RestauranteApp:

    def __init__(self):
        self.root = tk.Tk()
        self.servicio = RestauranteServicio()

        self.mostrar_login()
        self.root.mainloop()

    def limpiar_ventana(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def mostrar_login(self):
        self.limpiar_ventana()

        LoginView(
            self.root,
            self.servicio,
            self.mostrar_main
        )

    def mostrar_main(self, usuario):
        self.limpiar_ventana()

        MainView(
            self.root,
            self.servicio,
            usuario,
            self.mostrar_login
        )


if __name__ == "__main__":
    RestauranteApp()