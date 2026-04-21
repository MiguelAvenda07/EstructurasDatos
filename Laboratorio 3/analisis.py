import time
import matplotlib.pyplot as plt
from Quadtree import *

def medir_tiempo_cercano():
    tamanios = [1000, 5000, 10000, 50000, 100000]
    tiempos_quadtree = []
    tiempos_bruta  = []

    for n in tamanios:
        datos = generar_datos(n, 0, 100000)
        arbol = crear_arbol(datos)
        objetivos = [(random.randint(0, 100000), random.randint(0, 100000)) for _ in range(3)]

        t_kd = []
        t_fb = []
        for objetivo in objetivos:
            inicio = time.time()
            busqueda_mas_cercano(arbol, objetivo)
            t_kd.append(time.time() - inicio)

            inicio = time.time()
            cercano_fuerza_bruta(datos, objetivo)
            t_fb.append(time.time() - inicio)

        tiempos_quadtree.append(sum(t_kd) / 3)
        tiempos_bruta.append(sum(t_fb) / 3)

    return tamanios, tiempos_quadtree, tiempos_bruta


def medir_tiempo_radio():
    radios = [500, 1000, 5000, 10000, 20000, 30000, 50000, 100000]
    tiempos_kdtree = []
    tiempos_bruta  = []

    datos = generar_datos(10000, 0, 100000)
    arbol = crear_arbol(datos)
    centros = [(random.randint(0, 100000), random.randint(0, 100000)) for _ in range(3)]

    for radio in radios:
        t_kd = []
        t_fb = []
        for centro in centros:
            inicio = time.time()
            busqueda_radio(arbol, centro, radio)
            t_kd.append(time.time() - inicio)

            inicio = time.time()
            radio_fuerza_bruta(datos, centro, radio)
            t_fb.append(time.time() - inicio)

        tiempos_kdtree.append(sum(t_kd) / 3)
        tiempos_bruta.append(sum(t_fb) / 3)

    return radios, tiempos_kdtree, tiempos_bruta


def graficar_rendimiento():
    tamanios, t_quad_cercano, t_fb_cercano = medir_tiempo_cercano()
    radios,   t_quad_radio,   t_fb_radio   = medir_tiempo_radio()

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    # Gráfico 1: punto más cercano
    ax1.plot(tamanios, t_quad_cercano, marker='o', color='blue',   label='Quadtree')
    ax1.plot(tamanios, t_fb_cercano, marker='o', color='orange', label='Fuerza bruta')
    ax1.set_xlabel('Cantidad de puntos')
    ax1.set_ylabel('Tiempo (segundos)')
    ax1.set_title('Punto más cercano')
    ax1.legend()
    ax1.grid(True, linewidth=0.4)

    # Gráfico 2: búsqueda por radio
    ax2.plot(radios, t_quad_radio, marker='o', color='blue',   label='Quadtree')
    ax2.plot(radios, t_fb_radio, marker='o', color='orange', label='Fuerza bruta')
    ax2.set_xlabel('Radio')
    ax2.set_ylabel('Tiempo (segundos)')
    ax2.set_title('Búsqueda por radio (10,000 puntos)')
    ax2.legend()
    ax2.grid(True, linewidth=0.4)

    plt.suptitle('Quadtree vs Fuerza bruta', fontsize=13)
    plt.tight_layout()
    plt.show()

    # Imprimir resumen
    print("=== Punto más cercano ===")
    print(f"{'Tamaño':<10} {'Quadtree (s)':<15} {'Fuerza bruta (s)':<18}")
    for i in range(len(tamanios)):
        print(f"{tamanios[i]:<10} {t_quad_cercano[i]:<15.6f} {t_fb_cercano[i]:<18.6f}")

    print("\n=== Búsqueda por radio ===")
    print(f"{'Radio':<10} {'Quadtree (s)':<15} {'Fuerza bruta (s)':<18}")
    for i in range(len(radios)):
        
        print(f"{radios[i]:<10} {t_quad_radio[i]:<15.6f} {t_fb_radio[i]:<18.6f}")


graficar_rendimiento()