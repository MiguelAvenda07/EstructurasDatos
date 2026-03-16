## CO-CREADO CON AYUDA DE HERRAMIENTAS DE INTELIGENCIA ARTIFICIAL GENERATIVA (Claude, GitHub Copilot)


# Utilidades para generar datos aleatorios y medir tiempos.
import random
import time

# Estructuras que se van a comparar.
import ArbolBP
import ArbolBST
import Listas

# Semilla fija para que la generación inicial de estudiantes sea reproducible.
random.seed(67)

# Nombres posibles para los estudiantes generados.
nombres = [
    "Ana", "Carlos", "María", "Luis", "Sofía", "Pedro", "Laura", "Diego", "Valentina",
    "Andrés", "Camila", "Sebastián", "Daniela", "Felipe", "Isabella", "Mateo", "Lucía",
    "Santiago", "Paula", "Tomás", "Mariana", "Alejandro", "Sara", "Nicolás", "Elena", "Miguel", "Samuel"
]


def generar_estudiantes(n=10000):
    # Crea n estudiantes con id único, nombre aleatorio y promedio aleatorio.
    ids = random.sample(range(1000, 99999), n)
    return [
        {
            "id": ids[i],
            "nombre": random.choice(nombres),
            "promedio": round(random.uniform(5.0, 10.0), 1),
        }
        for i in range(n)
    ]


def medir_tiempo(func):
    # Ejecuta una función y retorna cuánto tardó junto con su resultado.
    t0 = time.perf_counter()
    resultado = func()
    t1 = time.perf_counter()
    return t1 - t0, resultado


def mostrar_busqueda(titulo, ids_buscados, n_busquedas, encontrados, detalle=None):
    # Muestra un resumen corto de cada prueba y pausa antes de continuar.
    print(f"\n--- {titulo} ---")
    if detalle:
        print(detalle)
    print(f"Primeros 10 ids buscados: {ids_buscados[:10]}")
    print(f"Busquedas realizadas: {n_busquedas} | Encontrados: {len(encontrados)}")
    print("Primeros 5 encontrados:")
    for e in encontrados[:5]:
        print(f"  {e}")
    input("\nPresiona Enter para continuar...")


def imprimir_resultados(resultados):
    # Imprime la tabla final con los tiempos de cada estructura.
    print("\n=== Comparacion de tiempos (segundos) ===")
    print(f"{'Estructura':<18} {'Tipo de busqueda':<30} {'Tiempo':>10}")
    print("-" * 62)
    for estructura, tipo, tiempo in resultados:
        print(f"{estructura:<18} {tipo:<30} {tiempo:>10.6f}")


def main():
    # Parámetros principales de la comparación.
    n_estudiantes = 10000

    # Genera los datos de prueba y un id objetivo para la búsqueda simple.
    estudiantes = generar_estudiantes(n_estudiantes)
    random.seed(None)
    n_busquedas_aleatorias = random.randint(100, 2000)
    rango_min, rango_max = sorted((random.randint(1000, 99999), random.randint(1000, 99999)))
    n_primeros = random.randint(100, n_estudiantes // 2)
    id_objetivo = random.randint(1000, 99999)

    print(f"Total de estudiantes: {len(estudiantes)}")
    print(f"Busquedas aleatorias por prueba: {n_busquedas_aleatorias}")
    print(f"Rango aleatorio usado: {rango_min} - {rango_max}")
    print(f"Cantidad de primeros solicitados: {n_primeros}")

    # Construye las tres estructuras con el mismo conjunto de estudiantes.
    lista = Listas.Lista(estudiantes)

    bst = ArbolBST.ArbolBST()
    for est in estudiantes:
        bst.insertar(est)

    bplus = ArbolBP.ArbolBPlus(orden=50)
    for est in estudiantes:
        bplus.insertar(est)

    # Aquí se van guardando los tiempos para la comparación final.
    resultados = []

    # --- Lista ---
    t, res = medir_tiempo(lambda: lista.buscar(id_objetivo))
    resultados.append(("Lista", "Busqueda simple", t))
    mostrar_busqueda("Lista - Busqueda simple", [id_objetivo], 1, [res] if res else [])

    # En las demás pruebas se repite el mismo patrón: medir, guardar y mostrar.
    t, (ids, enc) = medir_tiempo(lambda: lista.buscar_aleatorios(n_busquedas_aleatorias))
    resultados.append(("Lista", "Aleatoria desordenada", t))
    mostrar_busqueda("Lista - Aleatoria desordenada", ids, n_busquedas_aleatorias, enc, f"Cantidad aleatoria de busquedas: {n_busquedas_aleatorias}")

    t, (ids, enc) = medir_tiempo(lambda: lista.buscar_aleatorios_organizado(n_busquedas_aleatorias))
    resultados.append(("Lista", "Aleatoria ordenada", t))
    mostrar_busqueda("Lista - Aleatoria ordenada", ids, n_busquedas_aleatorias, enc, f"Cantidad aleatoria de busquedas: {n_busquedas_aleatorias}")

    t, enc = medir_tiempo(lambda: lista.buscar_rango(rango_min, rango_max))
    resultados.append(("Lista", "Rango", t))
    mostrar_busqueda("Lista - Rango", [e["id"] for e in enc], rango_max - rango_min + 1, enc, f"Rango aleatorio consultado: {rango_min} - {rango_max}")

    t, enc = medir_tiempo(lambda: lista.primeros_estudiantes_organizados(n_primeros))
    resultados.append(("Lista", "Primeros n", t))
    mostrar_busqueda("Lista - Primeros n", [e["id"] for e in enc], n_primeros, enc, f"Cantidad aleatoria de primeros solicitados: {n_primeros}")

    # --- BST ---
    t, res = medir_tiempo(lambda: bst.buscar(id_objetivo))
    resultados.append(("BST", "Busqueda simple", t))
    mostrar_busqueda("BST - Busqueda simple", [id_objetivo], 1, [res] if res else [])

    t, (ids, enc) = medir_tiempo(lambda: bst.buscar_aleatorios(n_busquedas_aleatorias))
    resultados.append(("BST", "Aleatoria", t))
    mostrar_busqueda("BST - Aleatoria", ids, n_busquedas_aleatorias, enc, f"Cantidad aleatoria de busquedas: {n_busquedas_aleatorias}")

    t, enc = medir_tiempo(lambda: bst.buscar_rango(rango_min, rango_max))
    resultados.append(("BST", "Rango", t))
    mostrar_busqueda("BST - Rango", [n.id for n in enc], rango_max - rango_min + 1, enc, f"Rango aleatorio consultado: {rango_min} - {rango_max}")

    t, enc = medir_tiempo(lambda: bst.buscar_primeros(n_primeros))
    resultados.append(("BST", "Primeros n", t))
    mostrar_busqueda("BST - Primeros n", [n.id for n in enc], n_primeros, enc, f"Cantidad aleatoria de primeros solicitados: {n_primeros}")

    # --- Arbol B+ ---
    t, res = medir_tiempo(lambda: bplus.buscar(id_objetivo))
    resultados.append(("Arbol B+", "Busqueda simple", t))
    mostrar_busqueda("Arbol B+ - Busqueda simple", [id_objetivo], 1, [res] if res else [])

    t, (ids, enc) = medir_tiempo(lambda: bplus.buscar_aleatorios(n_busquedas_aleatorias))
    resultados.append(("Arbol B+", "Aleatoria", t))
    mostrar_busqueda("Arbol B+ - Aleatoria", ids, n_busquedas_aleatorias, enc, f"Cantidad aleatoria de busquedas: {n_busquedas_aleatorias}")

    t, enc = medir_tiempo(lambda: bplus.buscar_rango(rango_min, rango_max))
    resultados.append(("Arbol B+", "Rango", t))
    # En B+ se usa _id_estudiante para extraer el id de forma uniforme.
    mostrar_busqueda("Arbol B+ - Rango", [bplus._id_estudiante(e) for e in enc], rango_max - rango_min + 1, enc, f"Rango aleatorio consultado: {rango_min} - {rango_max}")

    t, enc = medir_tiempo(lambda: bplus.primeros_estudiantes(n_primeros))
    resultados.append(("Arbol B+", "Primeros n", t))
    mostrar_busqueda("Arbol B+ - Primeros n", [bplus._id_estudiante(e) for e in enc], n_primeros, enc, f"Cantidad aleatoria de primeros solicitados: {n_primeros}")

    imprimir_resultados(resultados)


# Ejecuta la prueba completa solo si este archivo se corre directamente.
if __name__ == "__main__":
    main()