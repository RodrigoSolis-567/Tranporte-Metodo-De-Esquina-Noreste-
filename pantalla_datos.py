# ==============================================================
#  CLASE 3: PANTALLA DATOS (Captura y edición de la matriz)
# ==============================================================

import tkinter as tk
from tkinter import messagebox

from constantes import MAX_TAMANO, FUENTE, NEGRITA, TITULO
from widgets import Desplazable
from metodo_noroeste import MetodoNoroeste


class PantallaDatos(tk.Frame):
    """Pantalla donde el usuario primero define las dimensiones (filas y columnas)
    y luego ingresa los nombres, costos, ofertas y demandas del problema."""

    def __init__(self, app):
        super().__init__(app.root)
        self.app = app

        # Listas con las variables Tkinter de cada casilla
        self.nom_o, self.nom_d = [], []
        self.costos, self.ofertas, self.demandas = [], [], []

        # Variables para capturar la cantidad de filas y columnas
        self.var_m = tk.StringVar(value="")
        self.var_n = tk.StringVar(value="")

        self.zona = None
        self.grid_entradas = {}

        # Paso 1 obligatorio: primero elegir dimensiones antes de mostrar la tabla
        self.mostrar_paso_dimensiones()

    def mostrar_paso_dimensiones(self):
        """Paso 1: Interfaz para que el usuario elija obligatoriamente
        la cantidad de filas (orígenes) y columnas (destinos)."""
        for w in self.winfo_children():
            w.destroy()

        contenedor = tk.Frame(self)
        contenedor.pack(expand=True, fill="both", padx=20, pady=20)

        # Títulos
        tk.Label(contenedor, text="Configuración de la Tabla", font=TITULO).pack(pady=(25, 6))
        tk.Label(contenedor,
                 text="Elige primero la cantidad de filas y columnas que deseas utilizar en tu problema:",
                 font=("Arial", 12)).pack(pady=(0, 25))

        # Tarjeta central estilizada
        tarjeta = tk.Frame(contenedor, relief="groove", bd=2, padx=35, pady=25, bg="#fafafa")
        tarjeta.pack(pady=10)

        # Campo para filas (orígenes)
        fila_m = tk.Frame(tarjeta, bg="#fafafa")
        fila_m.pack(fill="x", pady=10)
        tk.Label(fila_m, text="Cantidad de filas (Orígenes / Oferta):",
                 font=NEGRITA, bg="#fafafa", width=34, anchor="w").pack(side="left")
        ent_m = tk.Entry(fila_m, textvariable=self.var_m, width=6, justify="center", font=("Arial", 13, "bold"))
        ent_m.pack(side="left", padx=10)

        # Campo para columnas (destinos)
        fila_n = tk.Frame(tarjeta, bg="#fafafa")
        fila_n.pack(fill="x", pady=10)
        tk.Label(fila_n, text="Cantidad de columnas (Destinos / Demanda):",
                 font=NEGRITA, bg="#fafafa", width=34, anchor="w").pack(side="left")
        ent_n = tk.Entry(fila_n, textvariable=self.var_n, width=6, justify="center", font=("Arial", 13, "bold"))
        ent_n.pack(side="left", padx=10)

        # Nota de rango permitido
        tk.Label(tarjeta, text=f"(Ingresa números enteros del 1 al {MAX_TAMANO})",
                 font=("Arial", 10, "italic"), fg="#666666", bg="#fafafa").pack(pady=(4, 18))

        # Botón para continuar
        btn_crear = tk.Button(tarjeta, text="Generar tabla y continuar  →",
                              command=self.confirmar_dimensiones, font=("Arial", 13, "bold"),
                              bg="#a5d6a7", fg="black", padx=20, pady=8, cursor="hand2")
        btn_crear.pack(fill="x", pady=(8, 4))

        def enfocar(entrada):
            entrada.focus_set()
            entrada.select_range(0, tk.END)
            entrada.icursor(tk.END)
            return "break"

        def generar_tabla(e=None):
            self.confirmar_dimensiones()
            return "break"

        # Atajos de teclado en el paso de dimensiones:
        # - En filas: Enter o flechas (Arriba/Abajo) pasan a columnas
        # - En columnas: Enter genera la tabla; flechas (Arriba/Abajo) regresan a filas
        ent_m.bind("<Return>", lambda e: enfocar(ent_n))
        ent_m.bind("<KP_Enter>", lambda e: enfocar(ent_n))
        ent_m.bind("<Down>", lambda e: enfocar(ent_n))
        ent_m.bind("<Up>", lambda e: enfocar(ent_n))

        ent_n.bind("<Return>", generar_tabla)
        ent_n.bind("<KP_Enter>", generar_tabla)
        ent_n.bind("<Up>", lambda e: enfocar(ent_m))
        ent_n.bind("<Down>", lambda e: enfocar(ent_m))

        self.unbind("<Return>")
        self.unbind("<KP_Enter>")

        enfocar(ent_m)

        # Opciones secundarias
        botones_inf = tk.Frame(contenedor)
        botones_inf.pack(pady=20)

        tk.Button(botones_inf, text="← Volver al menú principal",
                  command=self.app.mostrar_menu, font=FUENTE, padx=14, pady=6).pack(pady=4)

    def confirmar_dimensiones(self):
        """Valida las dimensiones ingresadas y avanza a la generación de la tabla."""
        str_m = self.var_m.get().strip()
        str_n = self.var_n.get().strip()

        if not str_m or not str_n:
            messagebox.showwarning(
                "Faltan datos",
                "Primero debes ingresar la cantidad de filas y la cantidad de columnas para continuar."
            )
            return

        try:
            m = int(str_m)
            n = int(str_n)
            if not (1 <= m <= MAX_TAMANO and 1 <= n <= MAX_TAMANO):
                raise ValueError
        except ValueError:
            messagebox.showwarning(
                "Dimensiones inválidas",
                f"Escribe números enteros válidos del 1 al {MAX_TAMANO} para las filas y columnas."
            )
            return

        self.mostrar_paso_tabla(m, n)

    def mostrar_paso_tabla(self, m, n):
        """Paso 2: Muestra la matriz de costos con las dimensiones elegidas
        para que el usuario ingrese los valores numéricos."""
        for w in self.winfo_children():
            w.destroy()

        tk.Label(self, text="Problema de Transporte", font=TITULO).pack(pady=(10, 4))

        # Barra superior de botones
        abajo = tk.Frame(self)
        abajo.pack(fill="x", pady=4)

        tk.Button(abajo, text="Volver al menú", command=self.app.mostrar_menu, font=FUENTE,
                  cursor="hand2").pack(side="left", padx=12)
        tk.Button(abajo, text="Cambiar filas / columnas", command=self.mostrar_paso_dimensiones,
                  font=NEGRITA, cursor="hand2").pack(side="left", padx=4)
        tk.Button(abajo, text="RESOLVER (o presiona ENTER)", command=self.resolver, font=("Arial", 13, "bold"),
                  bg="#a5d6a7", fg="black", padx=20, pady=6, cursor="hand2").pack(side="right", padx=12)

        self.bind("<Return>", lambda e: self.resolver())
        self.bind("<KP_Enter>", lambda e: self.resolver())

        tk.Label(self, text=f"Tabla de {m} orígenes (filas) × {n} destinos (columnas). "
                            "Escribe en cada casilla el costo de envío unitario, oferta y demanda. "
                            "Puedes personalizar los nombres.",
                 font=("Arial", 10), wraplength=900, justify="left").pack(padx=12, pady=(2, 6))

        self.zona = Desplazable(self)
        self.zona.pack(fill="both", expand=True, padx=12, pady=4)
        self.ajustar(m, n)

    def ajustar(self, m, n):
        """Agrega o quita filas y columnas sin borrar lo que ya se escribió."""
        while len(self.nom_o) > m:
            self.nom_o.pop()
            self.costos.pop()
            self.ofertas.pop()
        while len(self.nom_d) > n:
            self.nom_d.pop()
            self.demandas.pop()
            for fila in self.costos:
                fila.pop()
        while len(self.nom_d) < n:
            self.nom_d.append(tk.StringVar(value=f"Destino {len(self.nom_d) + 1}"))
            self.demandas.append(tk.StringVar())
            for fila in self.costos:
                fila.append(tk.StringVar())
        while len(self.nom_o) < m:
            self.nom_o.append(tk.StringVar(value=f"Origen {len(self.nom_o) + 1}"))
            self.ofertas.append(tk.StringVar())
            self.costos.append([tk.StringVar() for _ in self.nom_d])

        self.var_m.set(str(m))
        self.var_n.set(str(n))
        self.dibujar()

    def dibujar(self):
        """Dibuja las casillas de entrada en la zona desplazable y conecta los atajos del teclado."""
        if not self.zona:
            return

        t = self.zona.interior
        for w in t.winfo_children():
            w.destroy()

        self.grid_entradas = {}
        m, n = len(self.nom_o), len(self.nom_d)

        # Destinos (Fila 0, Columnas 1 a n)
        for j in range(n):
            e_dest = tk.Entry(t, textvariable=self.nom_d[j], width=13, justify="center", font=NEGRITA)
            e_dest.grid(row=0, column=j + 1, padx=3, pady=3)
            self._vincular_entrada(e_dest, 0, j + 1)

        tk.Label(t, text="OFERTA", font=NEGRITA).grid(row=0, column=n + 1, padx=(14, 3))

        # Orígenes (Col 0), Costos (Cols 1 a n), Ofertas (Col n + 1)
        for i in range(m):
            e_orig = tk.Entry(t, textvariable=self.nom_o[i], width=14, font=NEGRITA)
            e_orig.grid(row=i + 1, column=0, padx=3, pady=3)
            self._vincular_entrada(e_orig, i + 1, 0)

            for j in range(n):
                e_cost = tk.Entry(t, textvariable=self.costos[i][j], width=13, justify="center", font=FUENTE)
                e_cost.grid(row=i + 1, column=j + 1, padx=3, pady=3)
                self._vincular_entrada(e_cost, i + 1, j + 1)

            e_oferta = tk.Entry(t, textvariable=self.ofertas[i], width=10, justify="center", font=FUENTE,
                                bg="#e8f0ff")
            e_oferta.grid(row=i + 1, column=n + 1, padx=(14, 3))
            self._vincular_entrada(e_oferta, i + 1, n + 1)

        # Demandas (Fila m + 1, Columnas 1 a n)
        tk.Label(t, text="DEMANDA", font=NEGRITA).grid(row=m + 1, column=0, pady=(12, 0))
        for j in range(n):
            e_dem = tk.Entry(t, textvariable=self.demandas[j], width=13, justify="center", font=FUENTE,
                             bg="#e8f0ff")
            e_dem.grid(row=m + 1, column=j + 1, padx=3, pady=(12, 0))
            self._vincular_entrada(e_dem, m + 1, j + 1)

        # Foco inicial automático en la primera casilla de costos (Fila 1, Columna 1)
        if (1, 1) in self.grid_entradas:
            self.after(60, self._enfocar_inicial)

    def _vincular_entrada(self, entry, r, c):
        """Registra la casilla en el mapa de navegación y conecta las flechas y ENTER."""
        self.grid_entradas[(r, c)] = entry
        entry.bind("<Up>", lambda e: self.navegar(r, c, "Up"))
        entry.bind("<Down>", lambda e: self.navegar(r, c, "Down"))
        entry.bind("<Left>", lambda e: self.navegar(r, c, "Left"))
        entry.bind("<Right>", lambda e: self.navegar(r, c, "Right"))
        entry.bind("<Return>", lambda e: self._al_presionar_enter())
        entry.bind("<KP_Enter>", lambda e: self._al_presionar_enter())

    def _al_presionar_enter(self):
        """Ejecuta la resolución al presionar Enter."""
        self.resolver()
        return "break"

    def _enfocar_inicial(self):
        """Pone el foco en la primera celda numérica al cargar la tabla."""
        if (1, 1) in self.grid_entradas:
            primera = self.grid_entradas[(1, 1)]
            primera.focus_set()
            primera.select_range(0, tk.END)
            primera.icursor(tk.END)

    def _asegurar_visible(self, widget):
        """Ajusta el scroll del lienzo si la casilla enfocada queda fuera de la vista."""
        if not self.zona:
            return
        try:
            lienzo = self.zona.lienzo
            self.update_idletasks()
            wy, wh = widget.winfo_y(), widget.winfo_height()
            wx, ww = widget.winfo_x(), widget.winfo_width()
            total_h = self.zona.interior.winfo_height()
            total_w = self.zona.interior.winfo_width()

            if total_h > 0:
                y0, y1 = lienzo.yview()
                t_frac = wy / total_h
                b_frac = (wy + wh) / total_h
                if t_frac < y0:
                    lienzo.yview_moveto(max(0.0, t_frac - 0.02))
                elif b_frac > y1:
                    lienzo.yview_moveto(min(1.0, b_frac - (y1 - y0) + 0.02))

            if total_w > 0:
                x0, x1 = lienzo.xview()
                l_frac = wx / total_w
                r_frac = (wx + ww) / total_w
                if l_frac < x0:
                    lienzo.xview_moveto(max(0.0, l_frac - 0.02))
                elif r_frac > x1:
                    lienzo.xview_moveto(min(1.0, r_frac - (x1 - x0) + 0.02))
        except Exception:
            pass

    def navegar(self, r, c, direccion):
        """Mueve el foco a la casilla contigua según la flecha presionada."""
        if not self.grid_entradas:
            return "break"

        target_pos = None

        if direccion == "Up":
            # 1. Buscar en la misma columna hacia arriba
            for nr in range(r - 1, -1, -1):
                if (nr, c) in self.grid_entradas:
                    target_pos = (nr, c)
                    break
            # 2. Si no hay en la misma columna, buscar columna más próxima en fila anterior
            if target_pos is None and r > 0:
                cols_fila = [col for (row, col) in self.grid_entradas.keys() if row == r - 1]
                if cols_fila:
                    nc = min(cols_fila, key=lambda x: abs(x - c))
                    target_pos = (r - 1, nc)

        elif direccion == "Down":
            # 1. Buscar en la misma columna hacia abajo
            max_r = max(row for (row, col) in self.grid_entradas.keys())
            for nr in range(r + 1, max_r + 1):
                if (nr, c) in self.grid_entradas:
                    target_pos = (nr, c)
                    break
            # 2. Si no hay en la misma columna, buscar columna más próxima en fila siguiente
            if target_pos is None:
                cols_fila = [col for (row, col) in self.grid_entradas.keys() if row == r + 1]
                if cols_fila:
                    nc = min(cols_fila, key=lambda x: abs(x - c))
                    target_pos = (r + 1, nc)

        elif direccion == "Left":
            # 1. Buscar hacia la izquierda en la misma fila
            cols_izq = [col for (row, col) in self.grid_entradas.keys() if row == r and col < c]
            if cols_izq:
                target_pos = (r, max(cols_izq))
            else:
                # 2. Pasar al final de la fila anterior
                filas_ant = [row for (row, col) in self.grid_entradas.keys() if row < r]
                if filas_ant:
                    prev_r = max(filas_ant)
                    cols_prev = [col for (row, col) in self.grid_entradas.keys() if row == prev_r]
                    target_pos = (prev_r, max(cols_prev))

        elif direccion == "Right":
            # 1. Buscar hacia la derecha en la misma fila
            cols_der = [col for (row, col) in self.grid_entradas.keys() if row == r and col > c]
            if cols_der:
                target_pos = (r, min(cols_der))
            else:
                # 2. Pasar al inicio de la fila siguiente
                filas_sig = [row for (row, col) in self.grid_entradas.keys() if row > r]
                if filas_sig:
                    next_r = min(filas_sig)
                    cols_next = [col for (row, col) in self.grid_entradas.keys() if row == next_r]
                    # Si venimos de datos numéricos y la fila siguiente tiene costos (c=1), entrar a c=1
                    if 1 in cols_next and c > 0:
                        target_pos = (next_r, 1)
                    else:
                        target_pos = (next_r, min(cols_next))

        if target_pos and target_pos in self.grid_entradas:
            widget = self.grid_entradas[target_pos]
            widget.focus_set()
            widget.select_range(0, tk.END)
            widget.icursor(tk.END)
            self._asegurar_visible(widget)

        return "break"


    def leer(self):
        """Valida todas las casillas. Si hay algún error, avisa con un mensaje descriptivo."""
        m, n = len(self.nom_o), len(self.nom_d)
        nom_o = [v.get().strip() or f"Origen {i + 1}" for i, v in enumerate(self.nom_o)]
        nom_d = [v.get().strip() or f"Destino {j + 1}" for j, v in enumerate(self.nom_d)]

        def pedir(variable, que):
            valor, error = MetodoNoroeste.leer_numero(variable.get())
            if error == "vacio":
                messagebox.showwarning("Falta un dato", f"Por favor, ingresa todos los datos en la tabla")
            elif error == "letras":
                messagebox.showwarning("Revisa los datos", f"{que[0].upper() + que[1:]} debe ser un número "
                                                           "(sin letras ni símbolos).")
            elif error == "negativo":
                messagebox.showwarning("Revisa los datos", f"{que[0].upper() + que[1:]} no puede ser negativo.")
            return valor

        oferta, demanda, costos = [], [], []
        for i in range(m):
            v = pedir(self.ofertas[i], f"la oferta de {nom_o[i]}")
            if v is None:
                return None
            oferta.append(v)

        for j in range(n):
            v = pedir(self.demandas[j], f"la demanda de {nom_d[j]}")
            if v is None:
                return None
            demanda.append(v)

        for i in range(m):
            fila = []
            for j in range(n):
                v = pedir(self.costos[i][j], f"el costo de {nom_o[i]} a {nom_d[j]}")
                if v is None:
                    return None
                fila.append(v)
            costos.append(fila)

        return {"nom_o": nom_o, "nom_d": nom_d, "costos": costos, "oferta": oferta, "demanda": demanda}

    def resolver(self):
        """Valida los datos y delega la resolución a la aplicación."""
        datos = self.leer()
        if datos is None:
            return
        self.app.resolver(datos)
