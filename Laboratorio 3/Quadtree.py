import random

from matplotlib.collections import PatchCollection

class Nodo:
    def __init__(self, minimos=None, maximos=None, medios=None):
        self.hijos = []  # NO, NE   , SO, SE
        self.minimos = minimos
        self.maximos = maximos
        self.medios = medios
        self.punto = None
        self.subdividido = False
    
    def subdividir(self):
        # x >= x medio, y >= y medio -> NO (hijo 1)
        # x < x medio, y >= y medio -> NE (hijo 2)
        # x < x medio, y < y medio -> SO (hijo 3)
        # x >= x medio, y < y medio -> SE (hijo 4)
        self.hijos.append(Nodo(minimos=(self.minimos[0], self.medios[1]), maximos=(self.medios[0], self.maximos[1]), 
                                medios=((self.minimos[0] + self.medios[0]) / 2, (self.medios[1]  + self.maximos[1]) / 2)))
        self.hijos.append(Nodo(minimos=(self.medios[0], self.medios[1]), maximos=(self.maximos[0], self.maximos[1]), 
                                medios=((self.medios[0] + self.maximos[0]) / 2, (self.medios[1]  + self.maximos[1]) / 2)))
        self.hijos.append(Nodo(minimos=(self.minimos[0], self.minimos[1]), maximos=(self.medios[0], self.medios[1]), 
                                medios=((self.minimos[0] + self.medios[0]) / 2, (self.minimos[1]  + self.medios[1]) / 2)))
        self.hijos.append(Nodo(minimos=(self.medios[0], self.minimos[1]), maximos=(self.maximos[0], self.medios[1]), 
                                medios=((self.medios[0] + self.maximos[0]) / 2, (self.minimos[1]  + self.medios[1]) / 2)))
        self.subdividido = True

    def __repr__(self):
        return f"{self.punto}"

def crear_arbol(datos):
    if not datos:
        return None

    minimos = []
    maximos = []
    medios = []
    for eje in range(len(datos[0])):
        minimo = datos[0][eje]
        maximo = datos[-1][eje]
        for d in datos:
            if d[eje] < minimo:
                minimo = d[eje]
            if d[eje] > maximo:
                maximo = d[eje]
        medio = (minimo + maximo) /  2

        minimos.append(minimo)
        maximos.append(maximo)
        medios.append(medio)

    raiz = Nodo(minimos, maximos, medios)

    for dato in datos:
        insertar(raiz, dato)

    return raiz

def insertar(raiz, punto):
    if raiz.punto is None and not raiz.subdividido:
        raiz.punto = punto
    else:
        if not raiz.subdividido:
            punto_existente = raiz.punto
            raiz.punto = None
            raiz.subdividir()
            buscar_cuadrante(raiz, punto_existente)

        buscar_cuadrante(raiz, punto)


def buscar_cuadrante(raiz, punto):
        for hijo in raiz.hijos:
            if hijo and punto[0] >= hijo.minimos[0] and punto[0] < hijo.maximos[0] and punto[1] >= hijo.minimos[1] and punto[1] < hijo.maximos[1]:
                insertar(hijo, punto)
                break

def generar_datos(cantidad, min, max, dimensiones=2):
    random.seed(67)
    datos = []
    for i in range(cantidad):
        punto = tuple(random.randint(min, max) for _ in range(dimensiones))
        datos.append(punto)
    return datos

def busqueda_mas_cercano(raiz, objetivo):
    if raiz is None:
        return None, float('inf')
    
    if not raiz.subdividido:
        if raiz.punto is None:
            return None, float('inf')
        distancia = ((objetivo[0] - raiz.punto[0])**2 + (objetivo[1] - raiz.punto[1])**2) ** (1/2)
        return raiz.punto, distancia
    
    mejor_punto = None
    mejor_distancia = float('inf')

    hijos_ordenados = sorted(raiz.hijos, key=lambda hijo: distancia_bordes(hijo, objetivo))

    for hijo in hijos_ordenados:
        if distancia_bordes(hijo, objetivo) >= mejor_distancia:
            break

        punto_candidato, distancia_candidato = busqueda_mas_cercano(hijo, objetivo)
        if distancia_candidato < mejor_distancia:
            mejor_punto = punto_candidato
            mejor_distancia = distancia_candidato
    
    return mejor_punto, mejor_distancia

def distancia_bordes(raiz, objetivo):
    #Primero el minimo entre la coordenada x del objetivo y el maximo en x del cuadrante
    #Luego el máximo entre ese y el minimo de x para encontrar el punto en x del borde más cercano
    cerca_x = max(raiz.minimos[0], min(objetivo[0], raiz.maximos[0]))
    cerca_y = max(raiz.minimos[1], min(objetivo[1], raiz.maximos[1]))
    distancia_x = objetivo[0] - cerca_x
    distancia_y = objetivo[1] - cerca_y
    dist_minima = (distancia_x**2 + distancia_y**2) ** (1/2)
    return dist_minima

def busqueda_radio(raiz, objetivo, radio):
    if raiz is None:
        return None
    
    encontrados = []
    if not raiz.subdividido:
        if raiz.punto is not None:
            distancia = ((objetivo[0] - raiz.punto[0])**2 + (objetivo[1] - raiz.punto[1])**2) ** (1/2)
            if distancia <= radio:
                encontrados.append(raiz.punto)
        return encontrados

    for hijo in raiz.hijos:
        if distancia_bordes(hijo, objetivo) <= radio:
            encontrados += (busqueda_radio(hijo, objetivo, radio))

    return encontrados

def cercano_fuerza_bruta(datos, objetivo):
    mejor = None
    mejor_dist = float('inf')
    for p in datos:
        dist = (p[0] - objetivo[0])**2 + (p[1] - objetivo[1])**2
        if dist < mejor_dist:
            mejor_dist = dist
            mejor = p
    return mejor, mejor_dist**(1/2)

def radio_fuerza_bruta(datos, centro, radio):
    encontrados = []

    for p in datos:
        distancia = (p[0] - centro[0])**2 + (p[1] - centro[1])**2
        if distancia <= (radio)**2:
            encontrados.append(p)

    return encontrados

from matplotlib import patches
import matplotlib.pyplot as plt
def graficar_puntos(datos, arbol):
    x = [p[0] for p in datos]
    y = [p[1] for p in datos]

    fig, ax = plt.subplots(figsize=(8, 8))
    dibujar_cuadrantes(arbol, ax)  # <-- agregar esto
    ax.scatter(x, y, s=1, alpha=0.4, color='purple', label='Puntos')

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_title('Todos los puntos')
    ax.legend()
    ax.legend(loc='upper right')
    plt.tight_layout()
    plt.show()

COLORES = ['#ffd6d6', "#afcaef", "#bbf0bb", "#fbe7af",
           "#d8adf1", "#a9ddcf", "#d0a788", '#d6d6ff']

def dibujar_cuadrantes(nodo, ax, nivel=0, max_nivel=8):
    rects = []
    colores = []
    _recolectar_rects(nodo, rects, colores, nivel, max_nivel)
    col = PatchCollection(rects, facecolor=colores, edgecolor='gray', alpha=0.3, linewidth=0.5)
    ax.add_collection(col)

def _recolectar_rects(nodo, rects, colores, nivel, max_nivel):
    if nivel > max_nivel:
        return
    color = COLORES[nivel % len(COLORES)]
    ancho = nodo.maximos[0] - nodo.minimos[0]
    alto  = nodo.maximos[1] - nodo.minimos[1]
    rects.append(patches.Rectangle((nodo.minimos[0], nodo.minimos[1]), ancho, alto))
    colores.append(color)
    if nodo.subdividido:
        for hijo in nodo.hijos:
            _recolectar_rects(hijo, rects, colores, nivel + 1, max_nivel)

def graficar_mas_cercano(datos, objetivo, resultado, arbol):
    x = [p[0] for p in datos]
    y = [p[1] for p in datos]

    fig, ax = plt.subplots(figsize=(8, 8))
    dibujar_cuadrantes(arbol, ax)  # <-- agregar esto

    ax.scatter(x, y, s=1, alpha=0.3, color='purple', label='Puntos')
    ax.scatter(objetivo[0], objetivo[1], s=10, color='red', zorder=5, label=f'Objetivo: {objetivo}')
    ax.scatter(resultado[0], resultado[1], s=10, color='orange', zorder=5, label=f'Más cercano: {resultado}')
    ax.plot([objetivo[0], resultado[0]],
            [objetivo[1], resultado[1]],
            color='orange', linewidth=1, linestyle='--')

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_title('Punto más cercano')
    ax.legend(loc='upper right')
    plt.tight_layout()
    plt.show()

def graficar_radio(datos, centro, radio, encontrados, arbol):
    x = [p[0] for p in datos]
    y = [p[1] for p in datos]

    fig, ax = plt.subplots(figsize=(8, 8))
    dibujar_cuadrantes(arbol, ax)  # <-- agregar esto

    ax.scatter(x, y, s=1, alpha=0.3, color='purple', label='Puntos')

    xf = [n[0] for n in encontrados]
    yf = [n[1] for n in encontrados]
    ax.scatter(xf, yf, s=1, color='darkorange', zorder=5, label=f'Encontrados ({len(encontrados)})')
    ax.scatter(centro[0], centro[1], s=80, color='red', zorder=6, label=f'Centro: {centro}')

    circulo = patches.Circle(centro, radio,
                              linewidth=0.5, edgecolor='red',
                              facecolor='none')
    ax.add_patch(circulo)
    ax.set_aspect('equal')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_title(f'Búsqueda por radio ({radio})')
    ax.legend(loc='upper right')
    plt.tight_layout()
    plt.show()