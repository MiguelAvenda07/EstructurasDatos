class Nodo:
    def __init__(self, posicion):
        self.posicion = posicion
        self.derecha = None
        self.izquierda = None

    def __repr__(self):
        return f"{self.posicion}"


import random

def construir(datos, profundidad=0):
    raiz = None

    if not datos:
        return None

    if profundidad == 0:
        puntos = []
        for i in datos:
            puntos.append(Nodo(i))
    else:
        puntos = datos

    eje = profundidad % len(puntos[0].posicion)
    puntos.sort(key=lambda p: p.posicion[eje])

    mediana = len(puntos) // 2
    raiz = puntos[mediana]

    raiz.izquierda = construir(puntos[:mediana], profundidad + 1)
    raiz.derecha = construir(puntos[mediana+1:], profundidad + 1)

    return raiz

def generar_datos(cantidad, min, max, dimensiones=2):
    random.seed(67)
    datos = []
    for i in range(cantidad):
        punto = tuple(random.randint(min, max) for _ in range(dimensiones))
        datos.append(punto)
    return datos

def encontrar_mas_cercano(raiz, objetivo, profundidad = 0):
    if raiz is None:
        return None

    eje = profundidad % len(objetivo)
    mejor = raiz

    if objetivo[eje] >= raiz.posicion[eje]:
        rama_cercana = raiz.derecha
        rama_lejana = raiz.izquierda
    else:
        rama_cercana = raiz.izquierda
        rama_lejana = raiz.derecha

    candidato = encontrar_mas_cercano(rama_cercana, objetivo, profundidad + 1)
    if candidato is not None:
        dist_candidato = 0
        dist_mejor = 0
        for i in range(len(objetivo)):
            dist_candidato += (candidato.posicion[i] - objetivo[i])**2
            dist_mejor += (mejor.posicion[i]- objetivo[i])**2
        if dist_candidato < dist_mejor:
            mejor = candidato

    dist_mejor = 0
    for i in range(len(objetivo)):
        dist_mejor += (mejor.posicion[i] - objetivo[i])**2

    diferencia = (objetivo[eje] - raiz.posicion[eje])**2
    if diferencia < dist_mejor:
        candidato2 = encontrar_mas_cercano(rama_lejana, objetivo, profundidad + 1)
        if candidato2 is not None:
            dist_candidato2 = 0
            for i in range(len(objetivo)):
                dist_candidato2 += (candidato2.posicion[i] - objetivo[i])**2
            if dist_candidato2 < dist_mejor:
                mejor = candidato2

    return mejor

def encontrar_radio(raiz, centro, radio, profundidad = 0, encontrados = None):
    if encontrados is None:
        encontrados = []

    if raiz is None:
        return encontrados

    eje = profundidad % len(raiz.posicion)
    distancia = (raiz.posicion[0] - centro[0])**2 + (raiz.posicion[1] - centro[1])**2

    if distancia <= (radio)**2:
        encontrados.append(raiz)

    diferencia = centro[eje] - raiz.posicion[eje]
    if diferencia < 0:
        rama_cercana = raiz.izquierda
        rama_lejana = raiz.derecha
    else:
        rama_cercana = raiz.derecha
        rama_lejana = raiz.izquierda

    encontrar_radio(rama_cercana, centro, radio, profundidad+1, encontrados)

    if abs(diferencia) <= radio:
        encontrar_radio(rama_lejana, centro, radio, profundidad+1, encontrados)

    return encontrados

def cercano_fuerza_bruta(datos, objetivo):
    mejor = None
    mejor_dist = float('inf')
    for p in datos:
        dist = (p[0] - objetivo[0])**2 + (p[1] - objetivo[1])**2
        if dist < mejor_dist:
            mejor_dist = dist
            mejor = p
    return mejor

def radio_fuerza_bruta(datos, centro, radio):
    encontrados = []

    for p in datos:
        distancia = (p[0] - centro[0])**2 + (p[1] - centro[1])**2
        if distancia <= (radio)**2:
            encontrados.append(p)

    return encontrados

import matplotlib.pyplot as plt
import matplotlib.patches as patches

def graficar_puntos(datos, arbol):
    x = [p[0] for p in datos]
    y = [p[1] for p in datos]

    plt.figure(figsize=(8, 8))
    plt.scatter(x, y, s=1, alpha=0.4, color='purple', label='Puntos')
    plt.scatter(arbol.posicion[0], arbol.posicion[1], s=100, color='blue', zorder=6, marker='*', label='Raíz')

    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Todos los puntos')
    plt.legend()
    plt.tight_layout()
    plt.show()


def graficar_mas_cercano(datos, objetivo, resultado, arbol):
    x = [p[0] for p in datos]
    y = [p[1] for p in datos]

    plt.figure(figsize=(8, 8))
    plt.scatter(x, y, s=1, alpha=0.3, color='purple', label='Puntos')
    plt.scatter(arbol.posicion[0], arbol.posicion[1], s=100, color='blue', zorder=6, marker='*', label=f'Raíz: {arbol.posicion}')
    plt.scatter(objetivo[0], objetivo[1], s=80, color='red', zorder=5, label=f'Objetivo: {objetivo}')
    plt.scatter(resultado.posicion[0], resultado.posicion[1], s=80, color='orange', zorder=5, label=f'Más cercano: {resultado.posicion}')
    plt.plot([objetivo[0], resultado.posicion[0]],
             [objetivo[1], resultado.posicion[1]],
             color='orange', linewidth=1, linestyle='--')

    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Punto más cercano')
    plt.legend()
    plt.tight_layout()
    plt.show()


def graficar_radio(datos, centro, radio, encontrados, arbol):
    x = [p[0] for p in datos]
    y = [p[1] for p in datos]

    fig, ax = plt.subplots(figsize=(8, 8))
    ax.scatter(x, y, s=1, alpha=0.3, color='purple', label='Puntos')

    xf = [n.posicion[0] for n in encontrados]
    yf = [n.posicion[1] for n in encontrados]
    ax.scatter(xf, yf, s=1, color='darkorange', zorder=5, label=f'Encontrados ({len(encontrados)})')
    ax.scatter(centro[0], centro[1], s=80, color='red', zorder=6, label=f'Centro: {centro}')
    ax.scatter(arbol.posicion[0], arbol.posicion[1], s=100, color='blue', zorder=7, marker='*', label=f'Raíz: {arbol.posicion}')

    circulo = patches.Circle(centro, radio,
                              linewidth=0.5, edgecolor='red',
                              facecolor='none')
    ax.add_patch(circulo)
    ax.set_aspect('equal')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_title(f'Búsqueda por radio ({radio})')
    ax.legend()
    plt.tight_layout()
    plt.show()



