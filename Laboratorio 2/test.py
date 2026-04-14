## Pruebas unitarias ##

#Creación del arbol#

from KDtree import *

print("======= PRUEBAS UNITARIAS =======\n")

print("Construccion del arbol con datos vacíos")
datos = []
print(f"Datos: {datos}") ## Debe imprimir []
arbol = construir(datos)
print(f"Raiz: {arbol}\n") ## Debe imprimir None
input()

print("Construccion del arbol con datos no vacíos")
MIN = 0
MAX = 20000
CANTIDAD = 10000
datos = generar_datos(CANTIDAD, MIN, MAX) # Siempre son los mismos gracias a random.seed()
arbol = construir(datos)
print(f"Raiz: {arbol}\n") ## Debe imprimir la raíz del árbol
input()

print("Búsqueda del punto más cercano aleatorio")
## Generamos un punto objetivo aleatorio
random.seed()
objetivo = (random.randint(MIN, MAX), random.randint(MIN, MAX))
print(f"Objetivo: {objetivo}")
mas_cercano = encontrar_mas_cercano(arbol, objetivo)
print(f"Punto más cercano: {mas_cercano}\n") ## Debe imprimir el punto más cercano al objetivo
input()

print("Búsqueda del punto más cercano con fuerza bruta")
print(f"Objetivo: {objetivo}") ## Debe imprimir el mismo objetivo que la búsqueda con KD-tree
mas_cercano_fb = cercano_fuerza_bruta(datos, objetivo)
print(f"Punto más cercano (fuerza bruta): {mas_cercano_fb}\n") ## Debe imprimir el mismo punto que la búsqueda con KD-tree
input()

print("Búsqueda de puntos cercanos dentro de un radio para cualquier punto")
radio = 2000
print(f"Centro: {objetivo}, Radio: {radio}")
encontrados = encontrar_radio(arbol, objetivo, radio)
print(f"Puntos encontrados: {encontrados}\nTotal: {len(encontrados)}\n") ## Debe imprimir los puntos dentro del radio
input()

print("Búsqueda de puntos cercanos dentro de un radio con fuerza bruta")
print(f"Centro: {objetivo}, Radio: {radio}") ## Debe imprimir el mismo centro y radio que la búsqueda con KD-tree
encontrados_fb = radio_fuerza_bruta(datos, objetivo, radio)
print(f"Puntos encontrados (fuerza bruta): {encontrados_fb}\nTotal: {len(encontrados_fb)}\n") ## Debe imprimir los mismos puntos que la búsqueda con KD-tree
input()

print("======= VISUALIZACION =======")
graficar_puntos(datos, arbol)
graficar_mas_cercano(datos, objetivo, mas_cercano, arbol)
graficar_radio(datos, objetivo, radio, encontrados, arbol)