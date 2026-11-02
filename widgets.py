# ==============================================================
#  COMPONENTES Y WIDGETS PERSONALIZADOS
# ==============================================================

import tkinter as tk


class Desplazable(tk.Frame):
    """Una zona con barras de desplazamiento para tablas y contenidos grandes.
    Lo que se pone dentro va en self.interior."""

    def __init__(self, padre):
        super().__init__(padre)
        self.lienzo = tk.Canvas(self, highlightthickness=0)
        vertical = tk.Scrollbar(self, orient="vertical", command=self.lienzo.yview)
        horizontal = tk.Scrollbar(self, orient="horizontal", command=self.lienzo.xview)
        self.lienzo.configure(yscrollcommand=vertical.set, xscrollcommand=horizontal.set)
        
        vertical.pack(side="right", fill="y")
        horizontal.pack(side="bottom", fill="x")
        self.lienzo.pack(side="left", fill="both", expand=True)
        
        self.interior = tk.Frame(self.lienzo)
        self.lienzo.create_window((0, 0), window=self.interior, anchor="nw")
        self.interior.bind("<Configure>",
                           lambda e: self.lienzo.configure(scrollregion=self.lienzo.bbox("all")))
        self.bind_all("<MouseWheel>", self._rueda)

    def _rueda(self, evento):
        self.lienzo.yview_scroll(-1 if evento.delta > 0 else 1, "units")

    def destroy(self):
        self.unbind_all("<MouseWheel>")
        super().destroy()
