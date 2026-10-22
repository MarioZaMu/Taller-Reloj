"""Reloj analogico: logica (listas circulares) + interfaz tkinter."""

import math
import time            # hora del sistema (localtime) para el estado inicial
import tkinter as tk   # interfaz grafica (Canvas) de la biblioteca estandar

from lista_circular_doble import ListaCircularDoble


# ---------------------------------------------------------------- logica
class RelojLogico:
    """Tres listas circulares: segundos (60), minutos (60) y horas (12)."""

    def __init__(self):
        self.segundos = self._crear(60, 6.0)     # 360/60 grados por paso
        self.minutos = self._crear(60, 6.0)
        self.horas = self._crear(12, 30.0)       # 360/12 grados por paso

    @staticmethod
    def _crear(n, paso):
        lista = ListaCircularDoble()
        for i in range(n):
            lista.insertar(i, i * paso)
        return lista

    def fijar(self, h, m, s):
        self.horas.ir_a(h % 12)
        self.minutos.ir_a(m % 60)
        self.segundos.ir_a(s % 60)

    def hora_sistema(self):
        t = time.localtime()
        self.fijar(t.tm_hour, t.tm_min, t.tm_sec)

    def tick(self):
        """Avanza un segundo, con acarreo entre listas."""
        if self.segundos.avanzar():          # 59 -> 0
            if self.minutos.avanzar():       # 59 -> 0
                self.horas.avanzar()

    def tick_atras(self):
        """Retrocede un segundo, con prestamo entre listas."""
        if self.segundos.retroceder():       # 0 -> 59
            if self.minutos.retroceder():    # 0 -> 59
                self.horas.retroceder()

    def mover_minuto(self, sentido):
        """Ajuste manual: +1 / -1 minuto (con acarreo a horas)."""
        if sentido > 0:
            if self.minutos.avanzar():
                self.horas.avanzar()
        else:
            if self.minutos.retroceder():
                self.horas.retroceder()

    def mover_hora(self, sentido):
        (self.horas.avanzar if sentido > 0 else self.horas.retroceder)()

    def angulos(self):
        """Angulos de las tres manecillas. Hora y minuto incluyen el avance
        fraccionario para que se vean continuas, como en un reloj real."""
        a_s = self.segundos.actual.angulo
        a_m = self.minutos.actual.angulo + a_s / 60
        a_h = self.horas.actual.angulo + a_m / 12
        return a_h, a_m, a_s

    def texto(self):
        h = self.horas.actual.valor or 12
        return f"{h:02d}:{self.minutos.actual.valor:02d}:{self.segundos.actual.valor:02d}"


# ------------------------------------------------------------- interfaz
class RelojApp:
    TAM = 460
    C = TAM // 2
    R = 200
    ROMANOS = ["XII", "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI"]

    FONDO = "#10141c"
    CARATULA = "#f4efe6"
    BORDE = "#c9a24a"
    TINTA = "#1a1d24"
    SEGUNDERO = "#d63a2f"

    def __init__(self, raiz):
        self.raiz = raiz
        raiz.title("Reloj analogico - Lista circular doble")
        raiz.resizable(False, False)
        raiz.configure(bg=self.FONDO)

        self.logica = RelojLogico()
        self.logica.hora_sistema()
        self.corriendo = True
        self.sentido = 1           # 1 = adelante, -1 = atras

        self.canvas = tk.Canvas(raiz, width=self.TAM, height=self.TAM,
                                bg=self.FONDO, highlightthickness=0)
        self.canvas.pack(padx=10, pady=(10, 0))
        self.etiqueta = tk.Label(raiz, font=("Consolas", 16, "bold"),
                                 bg=self.FONDO, fg=self.BORDE)
        self.etiqueta.pack()
        self._crear_botones()
        self._atajos()

        self._dibujar_caratula()
        self._dibujar_manecillas()
        self.raiz.after(1000, self._ciclo)

    # ----- controles
    def _crear_botones(self):
        barra = tk.Frame(self.raiz, bg=self.FONDO)
        barra.pack(pady=8)
        botones = [
            ("<< Atras", self.alternar_sentido),
            ("Pausa", self.alternar_pausa),
            ("Hora -", lambda: self.ajustar("h", -1)),
            ("Hora +", lambda: self.ajustar("h", 1)),
            ("Min -", lambda: self.ajustar("m", -1)),
            ("Min +", lambda: self.ajustar("m", 1)),
            ("Ahora", self.sincronizar),
        ]
        self.botones = {}
        for texto, cmd in botones:
            b = tk.Button(barra, text=texto, command=cmd, width=8,
                          bg="#232a38", fg="white", relief="flat",
                          activebackground=self.BORDE)
            b.pack(side="left", padx=2)
            self.botones[texto] = b

    def _atajos(self):
        r = self.raiz
        r.bind("<Left>", lambda e: self.alternar_sentido())
        r.bind("<space>", lambda e: self.alternar_pausa())
        r.bind("<Up>", lambda e: self.ajustar("h", 1))
        r.bind("<Down>", lambda e: self.ajustar("h", -1))
        r.bind("<Right>", lambda e: self.ajustar("m", 1))
        r.bind("<a>", lambda e: self.ajustar("m", -1))
        r.bind("<n>", lambda e: self.sincronizar())

    def alternar_sentido(self):
        self.sentido *= -1
        self.botones["<< Atras"].config(
            text="Adelante >>" if self.sentido < 0 else "<< Atras")

    def alternar_pausa(self):
        self.corriendo = not self.corriendo
        self.botones["Pausa"].config(text="Seguir" if not self.corriendo else "Pausa")

    def ajustar(self, que, sentido):
        (self.logica.mover_hora if que == "h" else self.logica.mover_minuto)(sentido)
        self._dibujar_manecillas()

    def sincronizar(self):
        self.logica.hora_sistema()
        self._dibujar_manecillas()

    # ----- ciclo de tiempo
    def _ciclo(self):
        if self.corriendo:
            if self.sentido > 0:
                self.logica.tick()
            else:
                self.logica.tick_atras()
            self._dibujar_manecillas()
        self.raiz.after(1000, self._ciclo)

    # ----- dibujo
    def _punto(self, angulo, radio):
        """Convierte angulo (0 = arriba, horario) y radio en coordenadas."""
        rad = math.radians(angulo)
        return self.C + radio * math.sin(rad), self.C - radio * math.cos(rad)

    def _dibujar_caratula(self):
        c, C, R = self.canvas, self.C, self.R
        c.create_oval(C - R - 14, C - R - 14, C + R + 14, C + R + 14,
                      fill=self.BORDE, outline="")
        c.create_oval(C - R, C - R, C + R, C + R, fill=self.CARATULA,
                      outline=self.TINTA, width=2)
        for i in range(60):
            grande = i % 5 == 0
            x1, y1 = self._punto(i * 6, R - (16 if grande else 8))
            x2, y2 = self._punto(i * 6, R - 3)
            c.create_line(x1, y1, x2, y2, fill=self.TINTA,
                          width=3 if grande else 1)
        for i, num in enumerate(self.ROMANOS):
            x, y = self._punto(i * 30, R - 38)
            c.create_text(x, y, text=num, fill=self.TINTA,
                          font=("Georgia", 16, "bold"))
        c.create_text(C, C - 70, text="LISTA CIRCULAR", fill="#8a8578",
                      font=("Georgia", 9, "bold"))

    def _dibujar_manecillas(self):
        c, C = self.canvas, self.C
        c.delete("manecilla")
        a_h, a_m, a_s = self.logica.angulos()

        def mano(ang, largo, grosor, color, cola=0):
            x1, y1 = self._punto(ang + 180, cola)
            x2, y2 = self._punto(ang, largo)
            c.create_line(x1, y1, x2, y2, fill=color, width=grosor,
                          capstyle="round", tags="manecilla")

        mano(a_h, 100, 8, self.TINTA, 12)
        mano(a_m, 150, 5, self.TINTA, 14)
        mano(a_s, 170, 2, self.SEGUNDERO, 28)
        c.create_oval(C - 8, C - 8, C + 8, C + 8, fill=self.SEGUNDERO,
                      outline=self.TINTA, tags="manecilla")
        self.etiqueta.config(text=self.logica.texto())
