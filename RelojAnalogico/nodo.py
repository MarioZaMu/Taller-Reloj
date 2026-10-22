"""Nodo de una lista circular doblemente enlazada."""


class Nodo:
    """Guarda un valor y los enlaces a sus vecinos.

    En el reloj, `valor` es un diccionario/numero con la posicion (p. ej. el
    segundo 0..59) y `angulo` es el angulo en grados con el que se dibuja la
    manecilla cuando este nodo es el "actual".
    """

    def __init__(self, valor, angulo=0.0):
        self.valor = valor
        self.angulo = angulo      # grados, 0 = las 12, crece en sentido horario
        self.siguiente = None     # nodo posterior
        self.anterior = None      # nodo previo

    def __repr__(self):
        return f"Nodo(valor={self.valor!r}, angulo={self.angulo})"
