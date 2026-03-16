import time
import random

random.seed(None)


# Estructura simple basada en una lista de estudiantes.
class Lista:
   
    # Guarda directamente la colección recibida.
    def __init__(self, estudiantes): 
        self.lista = estudiantes
        
    # Inserta un nuevo estudiante al final de la lista.
    def insertar(self, estudiante): 
        self.lista.append(estudiante)

    # Busqueda secuencial: recorre toda la lista hasta encontrar el id.
    def buscar(self, k):
        for estudiante in self.lista:
            if estudiante["id"] == k:
                return estudiante
        return None
    
    # Ordena la lista por id y devuelve una nueva version ordenada.
    def listar(self):
        lista_ordenada = sorted(self.lista, key=lambda x: x["id"])
        return lista_ordenada

    # Recorre la lista completa y guarda los estudiantes dentro del rango pedido.
    def buscar_rango(self, minimo, maximo):
        if minimo > maximo:
            minimo, maximo = maximo, minimo

        encontrados = []
        for estudiante in self.lista:
            if minimo <= estudiante["id"] <= maximo:
                encontrados.append(estudiante)
        return encontrados
    
    # Toma los primeros n elementos tal como estan almacenados actualmente.
    def primeros_estudiantes(self, n):
        return self.lista[:n]

    # Primero ordena por id y luego devuelve los primeros n.
    def primeros_estudiantes_organizados(self, n):  
        lista_ordenada = self.listar()
        return lista_ordenada[:n]
    
    # Genera ids al azar y reutiliza la busqueda secuencial para ver cuales existen.
    def buscar_aleatorios(self, m):
        ids = random.sample(range(1000, 99999), m)

        encontrados = []
        for k in ids:
            if self.buscar(k) is not None:
                encontrados.append(self.buscar(k))
        return ids, encontrados

    # Hace lo mismo que la prueba anterior, pero sobre una copia ordenada de la lista.
    def buscar_aleatorios_organizado(self, m):
        ids = random.sample(range(1000, 99999), m)

        encontrados = []
        lista_ordenada = Lista(self.listar())
        
        for k in ids:
            if lista_ordenada.buscar(k) is not None:
                encontrados.append(lista_ordenada.buscar(k))
        return ids, encontrados


###lista_estudiantes = Lista(estudiantes)
#lista_estudiantes.buscar_aleatorios()
#lista_estudiantes.buscar_aleatorios_organizado()