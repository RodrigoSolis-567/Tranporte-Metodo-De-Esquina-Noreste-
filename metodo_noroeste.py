# ==============================================================
#  CLASE 1: METODO NOROESTE (Lógica matemática y modelo)
# ==============================================================

from decimal import Decimal, InvalidOperation


class MetodoNoroeste:
    """Encapsula el modelo del problema de transporte y el algoritmo
    de la Esquina Noroeste (balanceo, asignaciones, pasos y costos)."""

    def __init__(self, datos):
        """Inicializa el modelo con los datos del problema:
        nom_o: nombres de orígenes
        nom_d: nombres de destinos
        costos: matriz de costos unitarios
        oferta: lista de cantidades ofertadas
        demanda: lista de cantidades demandadas"""
        self.costos = [fila[:] for fila in datos["costos"]]
        self.oferta = list(datos["oferta"])
        self.demanda = list(datos["demanda"])
        self.nom_o = list(datos["nom_o"])
        self.nom_d = list(datos["nom_d"])

    @staticmethod
    def leer_numero(texto):
        """Convierte lo que escribió el usuario en un número Decimal exacto.
        Devuelve (numero, None) si es válido, o (None, motivo) si hay error."""
        t = texto.strip().replace(",", ".")
        if t == "":
            return None, "vacio"
        try:
            v = Decimal(t)
        except InvalidOperation:
            return None, "letras"
        if not v.is_finite():
            return None, "letras"
        if v < 0:
            return None, "negativo"
        return v, None

    @staticmethod
    def fmt(v):
        """Muestra los números formateados limpiamente: 35 en lugar de 35.0."""
        v = Decimal(v)
        if v == v.to_integral_value():
            return str(int(v))
        return format(v.normalize(), "f")

    def esta_balanceado(self):
        """Verifica si la suma de la oferta es igual a la suma de la demanda.
        Devuelve (balanceado, suma_oferta, suma_demanda, diferencia, descripcion_ficticio)."""
        so = sum(self.oferta)
        sd = sum(self.demanda)
        dif = abs(so - sd)
        cual = ("una columna ficticia (un destino inventado)" if so > sd
                else "una fila ficticia (un origen inventado)")
        return (so == sd, so, sd, dif, cual)

    def balancear(self):
        """Si oferta y demanda son distintas, agrega una fila o columna ficticia
        con costos 0. Devuelve el texto explicativo del balanceo."""
        so = sum(self.oferta)
        sd = sum(self.demanda)
        dif = abs(so - sd)

        if so > sd:
            for fila in self.costos:
                fila.append(Decimal(0))
            self.demanda.append(dif)
            self.nom_d.append("Destino ficticio")
            texto = (f"Hay más oferta ({self.fmt(so)}) que demanda ({self.fmt(sd)}), o sea que sobran {self.fmt(dif)} unidades.\n"
                     f"Se agregó una COLUMNA ficticia llamada «Destino ficticio» que pide esas {self.fmt(dif)} unidades.\n"
                     "Sus costos son 0, por eso no cambia el costo total. Lo que se asigne a esa columna "
                     "en realidad se queda sin enviar.")
        else:
            self.costos.append([Decimal(0)] * len(self.demanda))
            self.oferta.append(dif)
            self.nom_o.append("Origen ficticio")
            texto = (f"Hay más demanda ({self.fmt(sd)}) que oferta ({self.fmt(so)}), o sea que faltan {self.fmt(dif)} unidades.\n"
                     f"Se agregó una FILA ficticia llamada «Origen ficticio» que ofrece esas {self.fmt(dif)} unidades.\n"
                     "Sus costos son 0, por eso no cambia el costo total. Lo que se asigne a esa fila "
                     "en realidad no se podrá entregar.")
        return texto

    def ejecutar_algoritmo(self):
        """Aplica el método de la esquina noroeste comenzando en (0, 0).
        Devuelve (pasos, matriz_asignaciones)."""
        R, C = len(self.oferta), len(self.demanda)
        ofe, dem = list(self.oferta), list(self.demanda)
        asign = [[None] * C for _ in range(R)]
        pasos = []
        i = j = 0

        while i < R and j < C:
            q = min(ofe[i], dem[j])
            p = {"i": i, "j": j, "q": q, "o_antes": ofe[i], "d_antes": dem[j]}
            asign[i][j] = q
            ofe[i] -= q
            dem[j] -= q
            p["o_desp"], p["d_desp"] = ofe[i], dem[j]

            if i == R - 1 and j == C - 1:
                p["mov"] = "fin"
                i += 1
            elif ofe[i] == 0 and dem[j] == 0:
                p["mov"] = "ambos"
                i += 1
            elif ofe[i] == 0:
                p["mov"] = "abajo"
                i += 1
            else:
                p["mov"] = "derecha"
                j += 1
            pasos.append(p)

        return pasos, asign

    @classmethod
    def texto_paso(cls, num, p, nom_o, nom_d):
        """Genera una explicación comprensible en texto para un paso específico."""
        o, d = nom_o[p["i"]], nom_d[p["j"]]
        titulo = f"Paso {num}:"
        t = (f"Estamos en {o} - {d}.\n"
             f"A {o} le quedan {cls.fmt(p['o_antes'])} por enviar y a {d} le faltan {cls.fmt(p['d_antes'])} por recibir.\n"
             f"Se asigna el menor de los dos: {cls.fmt(p['q'])}.\n"
             f"Ahora a {o} le quedan {cls.fmt(p['o_desp'])} y a {d} le faltan {cls.fmt(p['d_desp'])}.\n")
        if p["mov"] == "fin":
            t += "Esta era la última celda. Ya se repartió todo.\n"
        elif p["mov"] == "abajo":
            t += f"Como {o} ya no tiene más para enviar, bajamos a la siguiente fila.\n"
        elif p["mov"] == "derecha":
            t += f"Como {d} ya quedó completo, nos movemos a la siguiente columna (a la derecha).\n"
        else:
            t += (f"A la vez se terminó lo que tenía {o} y lo que pedía {d}. Bajamos una fila; "
                  "la siguiente cantidad que se asigne será 0 para no saltarnos ninguna celda.\n")
        return titulo, t

    def resolver(self, info_balance=""):
        """Ejecuta el método y compila todos los resultados, cálculos y textos."""
        pasos, asign = self.ejecutar_algoritmo()
        total = Decimal(0)
        lineas, sumandos = [], []

        for i in range(len(self.nom_o)):
            for j in range(len(self.nom_d)):
                q = asign[i][j]
                if q is not None and q > 0:
                    parcial = q * self.costos[i][j]
                    total += parcial
                    lineas.append(f"{self.nom_o[i]} → {self.nom_d[j]}:   "
                                 f"{self.fmt(q)} × {self.fmt(self.costos[i][j])} = {self.fmt(parcial)}")
                    sumandos.append(self.fmt(parcial))

        if not sumandos:
            sumandos = ["0"]

        intro = (info_balance + "\n\nEl método empieza en la celda de arriba a la izquierda (la esquina noroeste). "
                 "En cada celda se asigna el menor entre lo que le queda por enviar al origen y lo que le falta "
                 "recibir al destino. Después se baja o se avanza a la derecha, según lo que se haya terminado.")

        datos_actuales = {
            "nom_o": self.nom_o,
            "nom_d": self.nom_d,
            "costos": self.costos,
            "oferta": self.oferta,
            "demanda": self.demanda
        }

        return {
            "datos": datos_actuales,
            "pasos": pasos,
            "asign": asign,
            "total": total,
            "lineas": lineas,
            "sumandos": sumandos,
            "balance": info_balance,
            "intro": intro
        }
