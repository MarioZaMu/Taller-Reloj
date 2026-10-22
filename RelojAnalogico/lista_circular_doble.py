"""Lista circular doblemente enlazada (implementacion propia)."""

from nodo import Nodo


class ListaCircularDoble:
    """Lista circular doble con un puntero `actual`.

    Invariante: si la lista no esta vacia, cabeza.anterior es la cola y
    cola.siguiente es la cabeza, de modo que siempre se puede girar.
    """

    def __init__(self):
        self.cabeza = None
        self.actual = None   # puntero de lectura (la "manecilla")
        self.tamano = 0

    def esta_vacia(self):
        return self.tamano == 0

    def __len__(self):
        return self.tamano

    # ---------- insercion / eliminacion ----------
    def insertar(self, valor, angulo=0.0):
        """Inserta un nodo al final (antes de la cabeza, en sentido circular)."""
        nuevo = Nodo(valor, angulo)
        if self.cabeza is None:
            nuevo.siguiente = nuevo
            nuevo.anterior = nuevo
            self.cabeza = nuevo
            self.actual = nuevo
        else:
            cola = self.cabeza.anterior
            cola.siguiente = nuevo
            nuevo.anterior = cola
            nuevo.siguiente = self.cabeza
            self.cabeza.anterior = nuevo
        self.tamano += 1
        return nuevo

    def eliminar(self, valor):
        """Elimina el primer nodo con ese valor. Devuelve True si lo encontro."""
        nodo = self.buscar(valor)
        if nodo is None:
            return False
        if self.tamano == 1:
            self.cabeza = self.actual = None
        else:
            nodo.anterior.siguiente = nodo.siguiente
            nodo.siguiente.anterior = nodo.anterior
            if nodo is self.cabeza:
                self.cabeza = nodo.siguiente
            if nodo is self.actual:
                self.actual = nodo.siguiente
        self.tamano -= 1
        return True

    def buscar(self, valor):
        """Devuelve el nodo con ese valor (o None)."""
        if self.cabeza is None:
            return None
        nodo = self.cabeza
        for _ in range(self.tamano):
            if nodo.valor == valor:
                return nodo
            nodo = nodo.siguiente
        return None

    # ---------- recorridos ----------
    def recorrer_adelante(self):
        """Lista de valores desde la cabeza siguiendo `siguiente` (una vuelta)."""
        resultado, nodo = [], self.cabeza
        for _ in range(self.tamano):
            resultado.append(nodo.valor)
            nodo = nodo.siguiente
        return resultado

    def recorrer_atras(self):
        """Lista de valores desde la cola siguiendo `anterior` (una vuelta)."""
        if self.cabeza is None:
            return []
        resultado, nodo = [], self.cabeza.anterior
        for _ in range(self.tamano):
            resultado.append(nodo.valor)
            nodo = nodo.anterior
        return resultado

    # ---------- puntero actual ----------
    def avanzar(self):
        """Mueve `actual` al siguiente nodo. Devuelve True si dio la vuelta
        completa (paso del ultimo al primero), util para el acarreo."""
        self.actual = self.actual.siguiente
        return self.actual is self.cabeza

    def retroceder(self):
        """Mueve `actual` al nodo anterior. Devuelve True si paso del primero
        al ultimo (prestamo)."""
        era_cabeza = self.actual is self.cabeza
        self.actual = self.actual.anterior
        return era_cabeza

    def ir_a(self, valor):
        """Coloca `actual` en el nodo con ese valor."""
        nodo = self.buscar(valor)
        if nodo is None:
            raise ValueError(f"valor {valor!r} no esta en la lista")
        self.actual = nodo
        return nodo
