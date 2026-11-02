import tkinter as tk
from decimal import Decimal

from constantes import FUENTE, NEGRITA, TEXTO, ROJO_SALIR, ROJO_SALIR_ACTIVO, BLANCO
from widgets import Desplazable
from metodo_noroeste import MetodoNoroeste


class PantallaResultado(tk.Frame):
    """Pantalla final con lógica precisa de bloqueo en rojo (0) para filas agotadas y columnas satisfechas."""

    def __init__(self, app, r):
        super().__init__(app.root)
        self.app = app
        self.r = r

        barra = tk.Frame(self)
        barra.pack(fill="x", padx=8, pady=8)

        self.b_res = tk.Button(barra, text="Ver resultado", command=self.ver_resultado,
                               font=NEGRITA, width=18, pady=6)
        self.b_pro = tk.Button(barra, text="Ver procedimiento", command=self.ver_procedimiento,
                               font=NEGRITA, width=18, pady=6)
        self.b_res.pack(side="left", padx=4)
        self.b_pro.pack(side="left", padx=4)

        tk.Button(barra, text="Salir", command=app.salir, font=NEGRITA,
                  bg=ROJO_SALIR, fg=BLANCO, activebackground=ROJO_SALIR_ACTIVO,
                  activeforeground=BLANCO, cursor="hand2", width=10, pady=6).pack(side="right", padx=4)
        tk.Button(barra, text="Nuevo problema", command=app.mostrar_datos, font=NEGRITA,
                  cursor="hand2", width=16, pady=6).pack(side="right", padx=4)

        self.area = tk.Frame(self)
        self.area.pack(fill="both", expand=True, padx=8, pady=4)
        self.ver_resultado()

    def limpiar(self):
        """Elimina los widgets del área central para cambiar de vista."""
        for w in self.area.winfo_children():
            w.destroy()

    # ==============================================================
    #  VISTA 1: PROCEDIMIENTO PASO A PASO
    # ==============================================================

    def ver_procedimiento(self):
        """Muestra el procedimiento paso a paso aplicando bloqueo en rojo (0) a filas y columnas agotadas."""
        self.limpiar()
        self.b_pro.config(relief="sunken")
        self.b_res.config(relief="raised")

        r = self.r
        d = r["datos"]
        nom_o = d["nom_o"]
        nom_d = d["nom_d"]
        costos = d["costos"]
        pasos = r["pasos"]
        R, C = len(nom_o), len(nom_d)

        oferta_ini = [Decimal(x) for x in d["oferta"]]
        demanda_ini = [Decimal(x) for x in d["demanda"]]

        zona = Desplazable(self.area)
        zona.pack(fill="both", expand=True)
        f = zona.interior

        tk.Label(f, text="Procedimiento Paso a Paso (Método de la Esquina Noroeste)",
                 font=("Arial", 16, "bold"), fg="#1565c0", anchor="w").pack(fill="x", padx=12, pady=(10, 4))

        barra_leyenda = tk.Frame(f, bg="#f8f9fa", relief="solid", bd=1, padx=10, pady=6)
        barra_leyenda.pack(fill="x", padx=12, pady=(4, 12))

        tk.Label(barra_leyenda, text="Guía:", font=NEGRITA, bg="#f8f9fa").pack(side="left", padx=(0, 10))
        tk.Label(barra_leyenda, text="  Asignación activa (Verde)  ", bg="#d4edda", fg="#155724", font=NEGRITA).pack(side="left", padx=4)
        tk.Label(barra_leyenda, text="  Agotado / Cero (Rojo)  ", bg="#f8d7da", fg="#721c24", font=NEGRITA).pack(side="left", padx=4)

        # ------------------------------------------------------------------
        # PASO 0: TABLA ORIGINAL / ESTADO INICIAL
        # ------------------------------------------------------------------
        card_ini = tk.Frame(f, bg="#ffffff", relief="groove", bd=2, padx=14, pady=10)
        card_ini.pack(fill="x", padx=12, pady=10)

        tk.Label(card_ini, text="Estado Inicial (Tabla Original del Problema)",
                 font=("Arial", 13, "bold"), fg="#333333", bg="#ffffff", anchor="w").pack(fill="x")

        marco_ini = tk.Frame(card_ini, bg="#6c757d", relief="solid", bd=1)
        marco_ini.pack(anchor="w", pady=(6, 6))

        tabla_ini = tk.Frame(marco_ini, bg="#6c757d")
        tabla_ini.pack(padx=1, pady=1)

        tk.Label(tabla_ini, text="", font=NEGRITA, bg="#f1f3f5", fg="#495057", width=16, height=2).grid(row=0, column=0, padx=1, pady=1)
        for j, col_nom in enumerate(nom_d):
            tk.Label(tabla_ini, text=col_nom, font=NEGRITA, bg="#f1f3f5", fg="#495057", width=18, height=2).grid(row=0, column=j + 1, padx=1, pady=1)
        tk.Label(tabla_ini, text="oferta", font=NEGRITA, bg="#f1f3f5", fg="#495057", width=12, height=2).grid(row=0, column=len(nom_d) + 1, padx=1, pady=1)

        for i, fil_nom in enumerate(nom_o):
            tk.Label(tabla_ini, text=fil_nom, font=NEGRITA, bg="#f1f3f5", fg="#495057", width=16, height=3).grid(row=i + 1, column=0, padx=1, pady=1)
            for j in range(len(nom_d)):
                costo_str = MetodoNoroeste.fmt(costos[i][j])
                tk.Label(tabla_ini, text=f"Costo: {costo_str}\nAsignación: -", bg="#ffffff", fg="#333333", width=18, height=3, font=FUENTE).grid(row=i + 1, column=j + 1, padx=1, pady=1)
            tk.Label(tabla_ini, text=MetodoNoroeste.fmt(oferta_ini[i]), font=NEGRITA, bg="#ffffff", fg="#212529", width=12, height=3).grid(row=i + 1, column=len(nom_d) + 1, padx=1, pady=1)

        tk.Label(tabla_ini, text="demanda", font=NEGRITA, bg="#f1f3f5", fg="#495057", width=16, height=2).grid(row=len(nom_o) + 1, column=0, padx=1, pady=1)
        for j in range(len(nom_d)):
            tk.Label(tabla_ini, text=MetodoNoroeste.fmt(demanda_ini[j]), font=NEGRITA, bg="#ffffff", fg="#212529", width=18, height=2).grid(row=len(nom_o) + 1, column=j + 1, padx=1, pady=1)
        tk.Label(tabla_ini, text=f"{MetodoNoroeste.fmt(sum(oferta_ini))}/{MetodoNoroeste.fmt(sum(demanda_ini))}", font=NEGRITA, bg="#ffffff", fg="#212529", width=12, height=2).grid(row=len(nom_o) + 1, column=len(nom_d) + 1, padx=1, pady=1)

        # ------------------------------------------------------------------
        # PASOS DEL ALGORITMO
        # ------------------------------------------------------------------
        asignaciones = [[None for _ in range(C)] for _ in range(R)]
        oferta_actual = list(oferta_ini)
        demanda_actual = list(demanda_ini)

        filas_agotadas = [False] * R
        cols_satisfechas = [False] * C

        for k, p in enumerate(pasos, 1):
            act_i, act_j, q = p["i"], p["j"], p["q"]
            asignaciones[act_i][act_j] = q
            oferta_actual[act_i] = p["o_desp"]
            demanda_actual[act_j] = p["d_desp"]

            # Verificar si la fila o columna se agotó en este paso
            if oferta_actual[act_i] == 0:
                filas_agotadas[act_i] = True
            if demanda_actual[act_j] == 0:
                cols_satisfechas[act_j] = True

            o_nom = nom_o[act_i]
            d_nom = nom_d[act_j]
            q_fmt = MetodoNoroeste.fmt(q)

            card = tk.Frame(f, bg="#ffffff", relief="groove", bd=2, padx=14, pady=10)
            card.pack(fill="x", padx=12, pady=10)

            texto_instruccion = f"Paso {k}: {o_nom} le asignó ${q_fmt} a {d_nom}"
            tk.Label(card, text=texto_instruccion,
                     font=("Arial", 13, "bold"), fg="#0d47a1", bg="#ffffff", anchor="w").pack(fill="x", pady=(0, 4))

            marco_tabla = tk.Frame(card, bg="#6c757d", relief="solid", bd=1)
            marco_tabla.pack(anchor="w", pady=(4, 6))

            tabla = tk.Frame(marco_tabla, bg="#6c757d")
            tabla.pack(padx=1, pady=1)

            tk.Label(tabla, text="", font=NEGRITA, bg="#f1f3f5", fg="#495057",
                     width=16, height=2).grid(row=0, column=0, padx=1, pady=1)

            for j, col_nom in enumerate(nom_d):
                tk.Label(tabla, text=col_nom, font=NEGRITA, bg="#f1f3f5", fg="#495057",
                         width=18, height=2).grid(row=0, column=j + 1, padx=1, pady=1)

            tk.Label(tabla, text="oferta", font=NEGRITA, bg="#f1f3f5", fg="#495057",
                     width=12, height=2).grid(row=0, column=len(nom_d) + 1, padx=1, pady=1)

            for i, fil_nom in enumerate(nom_o):
                tk.Label(tabla, text=fil_nom, font=NEGRITA, bg="#f1f3f5", fg="#495057",
                         width=16, height=3).grid(row=i + 1, column=0, padx=1, pady=1)

                for j in range(len(nom_d)):
                    val_q = asignaciones[i][j]
                    costo_str = MetodoNoroeste.fmt(costos[i][j])

                    if val_q is not None and val_q > 0:
                        bg_c, fg_c = "#d4edda", "#155724"  # Verde para celda activa con valor
                        txt_c = f"Costo: {costo_str}\nAsignación: {MetodoNoroeste.fmt(val_q)}"
                    elif val_q == 0:
                        bg_c, fg_c = "#f8d7da", "#721c24"  # Rojo explícito de 0
                        txt_c = f"Costo: {costo_str}\nAsignación: 0"
                    elif filas_agotadas[i] or cols_satisfechas[j]:
                        # Si la fila o columna ya se agotó/satisfechó, el resto se bloquea en rojo con 0
                        bg_c, fg_c = "#f8d7da", "#721c24"
                        txt_c = f"Costo: {costo_str}\nAsignación: 0"
                    else:
                        # Celda futura sin tocar
                        bg_c, fg_c = "#ffffff", "#333333"
                        txt_c = f"Costo: {costo_str}\nAsignación: -"

                    tk.Label(tabla, text=txt_c, bg=bg_c, fg=fg_c, font=FUENTE,
                             width=18, height=3).grid(row=i + 1, column=j + 1, padx=1, pady=1)

                tk.Label(tabla, text=MetodoNoroeste.fmt(oferta_actual[i]), font=NEGRITA, bg="#ffffff", fg="#212529",
                         width=12, height=3).grid(row=i + 1, column=len(nom_d) + 1, padx=1, pady=1)

            tk.Label(tabla, text="demanda", font=NEGRITA, bg="#f1f3f5", fg="#495057",
                     width=16, height=2).grid(row=len(nom_o) + 1, column=0, padx=1, pady=1)

            for j in range(len(nom_d)):
                tk.Label(tabla, text=MetodoNoroeste.fmt(demanda_actual[j]), font=NEGRITA, bg="#ffffff", fg="#212529",
                         width=18, height=2).grid(row=len(nom_o) + 1, column=j + 1, padx=1, pady=1)

            str_tot = f"{MetodoNoroeste.fmt(sum(oferta_actual))}/{MetodoNoroeste.fmt(sum(demanda_actual))}"
            tk.Label(tabla, text=str_tot, font=NEGRITA, bg="#ffffff", fg="#212529",
                     width=12, height=2).grid(row=len(nom_o) + 1, column=len(nom_d) + 1, padx=1, pady=1)

    # ==============================================================
    #  VISTA 2: RESULTADOS FINALES
    # ==============================================================

    def ver_resultado(self):
        """Muestra la tabla final aplicando bloqueo en rojo (0) a filas y columnas agotadas."""
        r = self.r
        d = r["datos"]
        nom_o, nom_d, costos = d["nom_o"], d["nom_d"], d["costos"]
        self.limpiar()
        self.b_res.config(relief="sunken")
        self.b_pro.config(relief="raised")

        zona = Desplazable(self.area)
        zona.pack(fill="both", expand=True)
        f = zona.interior

        def texto(contenido, fuente=FUENTE, color=TEXTO):
            tk.Label(f, text=contenido, font=fuente, fg=color, justify="left", anchor="w",
                     wraplength=880).pack(fill="x", padx=10, pady=2)

        texto(r["balance"], NEGRITA)
        texto("")

        # Rastrear qué filas y columnas terminaron agotadas en el resultado final
        oferta_actual = [Decimal(x) for x in d["oferta"]]
        demanda_actual = [Decimal(x) for x in d["demanda"]]
        
        # Simular avance para detectar filas y columnas agotadas
        filas_agotadas = [False] * len(nom_o)
        cols_satisfechas = [False] * len(nom_d)
        for p in r["pasos"]:
            if p["o_desp"] == 0:
                filas_agotadas[p["i"]] = True
            if p["d_desp"] == 0:
                cols_satisfechas[p["j"]] = True

        marco_tabla = tk.Frame(f, bg="#6c757d", relief="solid", bd=1)
        marco_tabla.pack(padx=10, pady=6, anchor="w")

        tabla = tk.Frame(marco_tabla, bg="#6c757d")
        tabla.pack(padx=1, pady=1)

        tk.Label(tabla, text="", font=NEGRITA, bg="#f1f3f5", fg="#495057",
                 width=16, height=2).grid(row=0, column=0, padx=1, pady=1)

        for j, nombre in enumerate(nom_d):
            tk.Label(tabla, text=nombre, font=NEGRITA, bg="#f1f3f5", fg="#495057",
                     width=18, height=2).grid(row=0, column=j + 1, padx=1, pady=1)
        
        tk.Label(tabla, text="oferta", font=NEGRITA, bg="#f1f3f5", fg="#495057",
                 width=12, height=2).grid(row=0, column=len(nom_d) + 1, padx=1, pady=1)

        for i, nombre in enumerate(nom_o):
            tk.Label(tabla, text=nombre, font=NEGRITA, bg="#f1f3f5", fg="#495057",
                     width=16, height=3).grid(row=i + 1, column=0, padx=1, pady=1)

            for j in range(len(nom_d)):
                q = r["asign"][i][j]
                costo_str = MetodoNoroeste.fmt(costos[i][j])

                if q is not None and q > 0:
                    bg_celda, fg_celda = "#d4edda", "#155724"  # Verde si tiene asignación activa
                    txt_celda = f"Costo: {costo_str}\nAsignación: {MetodoNoroeste.fmt(q)}"
                elif q == 0:
                    bg_celda, fg_celda = "#f8d7da", "#721c24"  # Rojo si se asignó 0 explícitamente
                    txt_celda = f"Costo: {costo_str}\nAsignación: 0"
                elif filas_agotadas[i] or cols_satisfechas[j]:
                    bg_celda, fg_celda = "#f8d7da", "#721c24"  # Rojo si la fila o columna se agotó
                    txt_celda = f"Costo: {costo_str}\nAsignación: 0"
                else:
                    bg_celda, fg_celda = "#ffffff", "#333333"  # Sin tocar
                    txt_celda = f"Costo: {costo_str}\nAsignación: -"

                tk.Label(tabla, text=txt_celda, bg=bg_celda, fg=fg_celda,
                         width=18, height=3, font=FUENTE).grid(row=i + 1, column=j + 1, padx=1, pady=1)
            
            tk.Label(tabla, text=MetodoNoroeste.fmt(d["oferta"][i]), font=NEGRITA, bg="#ffffff", fg="#212529",
                     width=12, height=3).grid(row=i + 1, column=len(nom_d) + 1, padx=1, pady=1)

        tk.Label(tabla, text="demanda", font=NEGRITA, bg="#f1f3f5", fg="#495057",
                 width=16, height=2).grid(row=len(nom_o) + 1, column=0, padx=1, pady=1)

        for j in range(len(nom_d)):
            tk.Label(tabla, text=MetodoNoroeste.fmt(d["demanda"][j]), font=NEGRITA, bg="#ffffff", fg="#212529",
                     width=18, height=2).grid(row=len(nom_o) + 1, column=j + 1, padx=1, pady=1)
        
        total_oferta_val = sum(Decimal(x) for x in d["oferta"])
        total_demanda_val = sum(Decimal(x) for x in d["demanda"])
        str_totales = f"{MetodoNoroeste.fmt(total_oferta_val)}/{MetodoNoroeste.fmt(total_demanda_val)}"

        tk.Label(tabla, text=str_totales, font=NEGRITA, bg="#ffffff", fg="#212529",
                 width=12, height=2).grid(row=len(nom_o) + 1, column=len(nom_d) + 1, padx=1, pady=1)

        texto("\nCantidades enviadas y su costo:", NEGRITA)
        for linea in r["lineas"]:
            texto(linea)
            
        texto(f"\nCosto Total = ${MetodoNoroeste.fmt(r['total'])}", ("Arial", 16, "bold"), "#155724")

        texto("\nPara ver el procedimiento detallado paso a paso con las tablas, presiona «Ver procedimiento».", ("Arial", 10), "#666666")