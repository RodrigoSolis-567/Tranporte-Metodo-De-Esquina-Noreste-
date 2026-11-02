# ==============================================================
#  CLASE 5: MAIN (Controlador principal y punto de entrada)
# ==============================================================

import tkinter as tk
from tkinter import messagebox

from metodo_noroeste import MetodoNoroeste
from pantalla_menu import PantallaMenu
from pantalla_datos import PantallaDatos
from pantalla_resultado import PantallaResultado


class Main:
    """Controlador principal de la aplicación: administra la ventana raíz,
    la navegación entre pantallas y coordina con el modelo matemático."""

    def __init__(self, root):
        self.root = root
        root.title("Método de la Esquina Noroeste")

        # La ventana se adapta dinámicamente a la resolución del monitor
        ancho = min(1000, root.winfo_screenwidth() - 40)
        alto = min(720, root.winfo_screenheight() - 100)
        root.geometry(f"{ancho}x{alto}+20+10")
        root.minsize(600, 450)

        self.pantalla = None
        self.mostrar_menu()

    def cambiar(self, crear_pantalla):
        """Reemplaza la pantalla actual por una nueva instancia."""
        if self.pantalla is not None:
            self.pantalla.destroy()
        self.pantalla = crear_pantalla()
        self.pantalla.pack(fill="both", expand=True)

    def mostrar_menu(self):
        """Muestra la pantalla de menú de inicio."""
        self.cambiar(lambda: PantallaMenu(self))

    def mostrar_datos(self):
        """Muestra la pantalla de captura de matriz y datos."""
        self.cambiar(lambda: PantallaDatos(self))

    def resolver(self, datos):
        """Coordina la verificación de balanceo con MetodoNoroeste
        y presenta los resultados al usuario."""
        metodo = MetodoNoroeste(datos)
        balanceado, so, sd, dif, cual = metodo.esta_balanceado()

        if balanceado:
            info = (f"El problema está balanceado. La oferta es igual a la Demanda ({MetodoNoroeste.fmt(so)}/{MetodoNoroeste.fmt(so)})\n"
                    "No fue necesario agregar filas ni columnas ficticias.")
        else:
            pregunta = (f"El problema no está balanceado.\n\n"
                        f"Oferta total: {MetodoNoroeste.fmt(so)}\n"
                        f"Demanda total: {MetodoNoroeste.fmt(sd)}\n"
                        f"Diferencia: {MetodoNoroeste.fmt(dif)}\n\n"
                        f"Para poder aplicar el método hay que agregar {cual} con costos de 0.\n"
                        "¿Quieres que lo haga automáticamente?")
            if not messagebox.askyesno("El problema no está balanceado", pregunta):
                return

            explicacion = metodo.balancear()
            info = (f"El problema no estaba balanceado. (Oferta total = {MetodoNoroeste.fmt(so)}, "
                    f"Demanda total = {MetodoNoroeste.fmt(sd)}, Diferencia = {MetodoNoroeste.fmt(dif)})\n"
                    f"{explicacion}")

        resultado = metodo.resolver(info)
        self.cambiar(lambda: PantallaResultado(self, resultado))

    def salir(self):
        """Cierra la aplicación limpiamente."""
        self.root.destroy()


if __name__ == "__main__":
    ventana = tk.Tk()
    Main(ventana)
    ventana.mainloop()
