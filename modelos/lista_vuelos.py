class Nodo:
    def __init__(self, vuelo):
        self.vuelo = vuelo
        self.anterior = None
        self.siguiente = None

class ListaDoblementeEnlazada:
    def __init__(self):
        self.primero = None
        self.ultimo = None
        self._longitud = 0

    def insertar_al_frente(self, vuelo):
        nuevo = Nodo(vuelo)
        if not self.primero:
            self.primero = self.ultimo = nuevo
        else:
            nuevo.siguiente = self.primero
            self.primero.anterior = nuevo
            self.primero = nuevo
        self._longitud += 1

    def insertar_al_final(self, vuelo):
        nuevo = Nodo(vuelo)
        if not self.ultimo:
            self.primero = self.ultimo = nuevo
        else:
            self.ultimo.siguiente = nuevo
            nuevo.anterior = self.ultimo
            self.ultimo = nuevo
        self._longitud += 1

    def obtener_primero(self):
        return self.primero.vuelo if self.primero else None

    def obtener_ultimo(self):
        return self.ultimo.vuelo if self.ultimo else None

    def longitud(self):
        return self._longitud

    def insertar_en_posicion(self, vuelo, pos):
        if pos < 0 or pos > self._longitud:
            raise IndexError("Posición fuera de rango")
        if pos == 0:
            self.insertar_al_frente(vuelo)
        elif pos == self._longitud:
            self.insertar_al_final(vuelo)
        else:
            nuevo = Nodo(vuelo)
            actual = self.primero
            for _ in range(pos):
                actual = actual.siguiente
            anterior = actual.anterior
            anterior.siguiente = nuevo
            nuevo.anterior = anterior
            nuevo.siguiente = actual
            actual.anterior = nuevo
            self._longitud += 1

    def extraer_de_posicion(self, pos):
        if pos < 0 or pos >= self._longitud:
            raise IndexError("Posición fuera de rango")
        actual = self.primero
        for _ in range(pos):
            actual = actual.siguiente
        if actual.anterior:
            actual.anterior.siguiente = actual.siguiente
        else:
            self.primero = actual.siguiente
        if actual.siguiente:
            actual.siguiente.anterior = actual.anterior
        else:
            self.ultimo = actual.anterior
        self._longitud -= 1
        return actual.vuelo
