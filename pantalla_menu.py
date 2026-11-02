# ==============================================================
#  CLASE 2: PANTALLA MENU (Menú de bienvenida)
# ==============================================================

import tkinter as tk
from constantes import ROJO_SALIR, ROJO_SALIR_ACTIVO, BLANCO


class PantallaMenu(tk.Frame):
    """Pantalla de inicio con las opciones principales del programa."""

    def __init__(self, app):
        super().__init__(app.root)
        self.app = app

        tk.Label(self, text="Método de la Esquina Noroeste", font=("Arial", 26, "bold")).pack(pady=(70, 6))
        tk.Label(self, text="Resuelve problemas de transporte paso a paso", font=("Arial", 13)).pack(pady=(0, 40))

        botones = [
            ("Resolver problema", app.mostrar_datos),
            ("Salir", app.salir)
        ]

        for texto, accion in botones:
            if texto == "Salir":
                tk.Button(self, text=texto, command=accion, font=("Arial", 15, "bold"),
                          bg=ROJO_SALIR, fg=BLANCO, activebackground=ROJO_SALIR_ACTIVO,
                          activeforeground=BLANCO, cursor="hand2", width=32, pady=12).pack(pady=8)
            else:
                tk.Button(self, text=texto, command=accion, font=("Arial", 15, "bold"),
                          cursor="hand2", width=32, pady=12).pack(pady=8)
