"""Pruebas simples: python test_lista.py"""

from lista_circular_doble import ListaCircularDoble
from reloj import RelojLogico


def lista_de(n):
    l = ListaCircularDoble()
    for i in range(n):
        l.insertar(i, i * 10)
    return l


def test_insercion():
    l = lista_de(5)
    assert len(l) == 5
    assert l.recorrer_adelante() == [0, 1, 2, 3, 4]
    assert l.cabeza.anterior.valor == 4      # cola
    assert l.cabeza.anterior.siguiente is l.cabeza


def test_recorrido_circular():
    l = lista_de(4)
    visitados = []
    for _ in range(9):                       # mas de dos vueltas
        visitados.append(l.actual.valor)
        l.avanzar()
    assert visitados == [0, 1, 2, 3, 0, 1, 2, 3, 0]


def test_retroceso():
    l = lista_de(4)
    assert l.recorrer_atras() == [3, 2, 1, 0]
    assert l.retroceder() is True            # 0 -> 3
    assert l.actual.valor == 3
    l.retroceder()
    assert l.actual.valor == 2
    l.avanzar()
    l.avanzar()
    assert l.actual.valor == 0               # ida y vuelta


def test_eliminar():
    l = lista_de(4)
    assert l.eliminar(2) is True
    assert l.recorrer_adelante() == [0, 1, 3]
    assert l.eliminar(0) is True             # elimina la cabeza
    assert l.cabeza.valor == 1 and l.cabeza.anterior.valor == 3
    assert l.eliminar(99) is False
    l.eliminar(1)
    l.eliminar(3)
    assert l.esta_vacia()


def test_reloj_acarreo():
    r = RelojLogico()
    r.fijar(11, 59, 59)
    r.tick()
    assert r.texto() == "12:00:00"          # 11:59:59 -> 12:00:00
    r.tick_atras()
    assert r.texto() == "11:59:59"
    r.fijar(12, 0, 0)
    a_h, a_m, a_s = r.angulos()
    assert (a_h, a_m, a_s) == (0, 0, 0)
    r.fijar(3, 0, 0)
    assert r.angulos()[0] == 90


if __name__ == "__main__":
    for nombre, f in list(globals().items()):
        if nombre.startswith("test_"):
            f()
            print("OK", nombre)
    print("Todas las pruebas pasaron")
