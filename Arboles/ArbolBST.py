import random

random.seed(None)


# Nodo del BST: guarda los datos del estudiante y dos referencias, una a la izquierda y otra a la derecha.
class Nodo:
    def __init__(self, estudiante):
        self.id = estudiante["id"]
        self.nombre = estudiante["nombre"]
        self.promedio = estudiante["promedio"]
        self.izquierda = None
        self.derecha = None
    
    def __repr__(self):
        return f"ID: {self.id} | Nombre: {self.nombre} | Promedio: {self.promedio}"


# Arbol binario de busqueda: menores a la izquierda, mayores a la derecha.
class ArbolBST:
    def __init__(self):
        self.raiz = None

    # Insercion: coloca cada estudiante segun su id, conservando la propiedad del BST.
    def insertar(self, estudiante):
        self.raiz = self._insertar(self.raiz, estudiante)

    # Baja recursivamente hasta encontrar el lugar correcto para crear el nuevo nodo.
    def _insertar(self, nodo, estudiante):
        if nodo is None:
            return Nodo(estudiante)
        if estudiante["id"] < nodo.id:
            nodo.izquierda = self._insertar(nodo.izquierda, estudiante)
        elif estudiante["id"] > nodo.id:
            nodo.derecha = self._insertar(nodo.derecha, estudiante)
        # Si el id ya existe, no se inserta de nuevo.
        return nodo
    
    # Busqueda normal en BST: compara el id y decide si seguir a izquierda o derecha.
    def buscar(self, id_estudiante):
        return self._buscar(self.raiz, id_estudiante)

    def _buscar(self, nodo, id_estudiante):
        if nodo is None:
            return None
        if id_estudiante == nodo.id:
            return nodo
        if id_estudiante < nodo.id:
            return self._buscar(nodo.izquierda, id_estudiante)
        return self._buscar(nodo.derecha, id_estudiante)

    # Busca todos los nodos entre dos ids, aprovechando que el arbol ya esta ordenado.
    def buscar_rango(self, minimo, maximo):
        if minimo > maximo:
            minimo, maximo = maximo, minimo
        resultado = []
        self._buscar_rango(self.raiz, minimo, maximo, resultado)
        return resultado

    # Solo entra a ramas que todavia podrian contener valores dentro del rango.
    def _buscar_rango(self, nodo, minimo, maximo, resultado):
        if nodo is None:
            return
        if nodo.id > minimo:
            self._buscar_rango(nodo.izquierda, minimo, maximo, resultado)
        if minimo <= nodo.id <= maximo:
            resultado.append(nodo)
        if nodo.id < maximo:
            self._buscar_rango(nodo.derecha, minimo, maximo, resultado)

    # Obtiene los primeros n elementos en orden ascendente usando recorrido inorden.
    def buscar_primeros(self, n):
        if n <= 0:
            return []
        resultado = []
        self._buscar_primeros(self.raiz, n, resultado)
        return resultado

    # El recorrido inorden visita: izquierda, nodo actual, derecha.
    def _buscar_primeros(self, nodo, n, resultado):
        if nodo is None or len(resultado) >= n:
            return
        self._buscar_primeros(nodo.izquierda, n, resultado)
        if len(resultado) < n:
            resultado.append(nodo)
        self._buscar_primeros(nodo.derecha, n, resultado)

    # Genera ids al azar y reutiliza la busqueda del arbol para ver cuales existen.
    def buscar_aleatorios(self, m):
        ids = random.sample(range(1000, 99999), m)
        encontrados = []
        for k in ids:
            if self.buscar(k):
                encontrados.append(self.buscar(k))
        return ids, encontrados

    
'''arbol_estudiantes = ArbolBST()
for estudiante in estudiantes:
    arbol_estudiantes.insertar(estudiante)
arbol_estudiantes.buscar_aleatorios()
'''