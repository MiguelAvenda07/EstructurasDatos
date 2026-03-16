import random

random.seed(None)


# Representa un estudiante individual dentro del arbol.
class Estudiante:
    def __init__(self, id, nombre, promedio):
        self.id       = id
        self.nombre   = nombre
        self.promedio = promedio

    def __repr__(self):
        return f"({self.id} | {self.nombre} | {self.promedio})"


# Nodo interno: no guarda estudiantes, solo claves guia y referencias a hijos.
class NodoInterno:
    def __init__(self):
        self.claves = []
        self.hijos = []
        self.es_hoja = False


# Nodo hoja: guarda los estudiantes reales y se enlaza con la siguiente hoja.
class NodoHoja:
    def __init__(self):
        self.claves = []
        self.hijos = []
        self.es_hoja = True
        self.siguiente = None


# Arbol B+: las hojas almacenan datos y los nodos internos solo dirigen la busqueda.
class ArbolBPlus:
    def __init__(self, orden):
        self.raiz  = NodoHoja()
        self.orden = orden

    # Convierte diccionarios a objetos Estudiante para manejar un solo formato interno.
    def _a_estudiante(self, estudiante):
        if isinstance(estudiante, Estudiante):
            return estudiante
        return Estudiante(estudiante["id"], estudiante["nombre"], estudiante["promedio"])

    # Extrae el id del estudiante (siempre es un objeto Estudiante dentro del arbol).
    def _id_estudiante(self, estudiante):
        return estudiante.id

    # Busqueda: primero baja hasta la hoja correcta y luego revisa los estudiantes de esa hoja.
    def buscar(self, id_estudiante):
        hoja = self._ir_a_hoja(self.raiz, id_estudiante)
        for est in hoja.hijos:
            if self._id_estudiante(est) == id_estudiante:
                return est
        return None

    # Recorre el arbol desde un nodo hasta llegar a la hoja donde deberia estar la clave.
    def _ir_a_hoja(self, nodo, clave):
        if nodo.es_hoja:
            return nodo
        for i, c in enumerate(nodo.claves):
            if clave < c:
                return self._ir_a_hoja(nodo.hijos[i], clave)
        return self._ir_a_hoja(nodo.hijos[-1], clave)

  

    # Insercion: agrega el estudiante y, si un nodo se llena demasiado, lo divide.
    def insertar(self, estudiante):
        estudiante = self._a_estudiante(estudiante)
        resultado = self._insertar(self.raiz, estudiante)
        if resultado:
            clave_media, hijo_derecho = resultado
            nueva_raiz = NodoInterno()
            nueva_raiz.claves = [clave_media]
            nueva_raiz.hijos  = [self.raiz, hijo_derecho]
            self.raiz = nueva_raiz

    # Inserta de forma recursiva hasta llegar a una hoja; luego propaga divisiones si hacen falta.
    def _insertar(self, nodo, estudiante):
        id_est = self._id_estudiante(estudiante)
        if nodo.es_hoja:
            # En hoja, se inserta y se reordena por id.
            nodo.hijos.append(estudiante)
            nodo.hijos.sort(key=self._id_estudiante)
            nodo.claves = [self._id_estudiante(e) for e in nodo.hijos]
            if len(nodo.hijos) > self.orden:
                return self._dividir_hoja(nodo)
            return None

        # En nodo interno, se elige el hijo correcto y se continua hacia abajo.
        i = len(nodo.claves)
        for j, c in enumerate(nodo.claves):
            if id_est < c:
                i = j
                break
        resultado = self._insertar(nodo.hijos[i], estudiante)
        if resultado:
            clave_media, hijo_derecho = resultado
            nodo.claves.insert(i, clave_media)
            nodo.hijos.insert(i + 1, hijo_derecho)
            if len(nodo.claves) > self.orden:
                return self._dividir_interno(nodo)
        return None

    # Divide una hoja en dos y enlaza la nueva hoja con la cadena de hojas.
    def _dividir_hoja(self, nodo):
        medio   = len(nodo.hijos) // 2
        hermano = NodoHoja()
        hermano.hijos    = nodo.hijos[medio:]
        hermano.claves   = [self._id_estudiante(e) for e in hermano.hijos]
        nodo.hijos       = nodo.hijos[:medio]
        nodo.claves      = [self._id_estudiante(e) for e in nodo.hijos]
        hermano.siguiente = nodo.siguiente
        nodo.siguiente    = hermano
        return hermano.claves[0], hermano

    # Divide un nodo interno y sube la clave central al nivel superior.
    def _dividir_interno(self, nodo):
        medio       = len(nodo.claves) // 2
        clave_media = nodo.claves[medio]
        hermano     = NodoInterno()
        hermano.claves = nodo.claves[medio + 1:]
        hermano.hijos  = nodo.hijos[medio + 1:]
        nodo.claves    = nodo.claves[:medio]
        nodo.hijos     = nodo.hijos[:medio + 1]
        return clave_media, hermano

    # Recorre las hojas de izquierda a derecha y guarda los ids dentro del rango pedido.
    # Salta directamente a la hoja donde empieza el rango en lugar de empezar desde el inicio.
    def buscar_rango(self, minimo, maximo):
        if minimo > maximo:
            minimo, maximo = maximo, minimo

        resultado = []
        terminar = False
        nodo = self._ir_a_hoja(self.raiz, minimo)

        while nodo and not terminar:
            for est in nodo.hijos:
                id_est = self._id_estudiante(est)
                if minimo <= id_est <= maximo:
                    resultado.append(est)
                elif id_est > maximo:
                    terminar = True
                    break
            nodo = nodo.siguiente
        return resultado

    # Genera ids al azar y reutiliza la busqueda normal para ver cuales existen.
    def buscar_aleatorios(self, n):
        ids = random.sample(range(1000, 99999), n)
        encontrados = []
        for id_estudiante in ids:
            est = self.buscar(id_estudiante)
            if est is not None:
                encontrados.append(est)
        return ids, encontrados

    # Obtiene los primeros n estudiantes ya ordenados, aprovechando el enlace entre hojas.
    def primeros_estudiantes(self, n):
        if n <= 0:
            return []

        estudiantes = []
        nodo = self.raiz

        while not nodo.es_hoja:
            nodo = nodo.hijos[0]

        while nodo is not None and len(estudiantes) < n:
            for est in nodo.hijos:
                estudiantes.append(est)
                if len(estudiantes) == n:
                    break
            nodo = nodo.siguiente
        return estudiantes

    # Recorre todas las hojas enlazadas y devuelve todos los estudiantes en orden.
    def ordenar(self):
        resultado = []
        nodo = self.raiz
        while not nodo.es_hoja:
            nodo = nodo.hijos[0]
        while nodo:
            resultado.extend(nodo.hijos)
            nodo = nodo.siguiente
        return resultado
    
'''arbol_bplus = ArbolBPlus(orden=3)
for estudiante in estudiantes:
    arbol_bplus.insertar(estudiante)

nodo = arbol_bplus.raiz
while not nodo.es_hoja:
    nodo = nodo.hijos[-1]

print(nodo.hijos[-1])   
'''