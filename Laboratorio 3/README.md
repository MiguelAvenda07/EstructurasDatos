# Laboratorio 3: Quadtree

Código cocreado con ayuda de Claude.

Este laboratorio tiene 3 archivos.

## 1. KDtree.py

Este archivo contiene la clase `Nodo`, necesaria para crear los árboles. No hay una clase árbol como tal, pues este se crea tomando el nodo raíz y guardándolo en una variable. Como ese nodo ya está ligado a todo el árbol con el atributo `hijos`, que es el arreglo que va a guardar todos los hijos en el orden NE, NO, SO, SE, consideré que no era necesario crear una clase entera cuyo único atributo fuera la raíz.

### Construcción del árbol

El árbol se construye con el método `crear_arbol()`, que recibe:

- una lista `datos` de parejas `(x, y)`

Se crean listas vacías que van a guardar los mínimos, máximos y el medio de cada uno de los ejes, recorriendo la lista comparando los dos ejes, buscando los maximos y los minimos y sacando el medio para añadirlos a la lista

Se crea una raiz con estos datos y se empiezan a insertar los datos

### Inserción de datos
Primero se revisa si la raiz no tiene hojas ni está subdividida, si se cumple la condicion, se inserta el dato en la hoja. Si no, se verifica que el nodo ya esté subdividido o en el caso contrario, se crean los cuatro hijos y la hoja que tiene se baja al hijo correspondiente, finalmente se baja el dato que se queria insertar desde el principio

El método `bajar_punto` recorre cada uno de los hijos del nodo para buscar en cual cuadrante se va a insertar el dato, esto se hace verificando que las coordenadas del dato estén dentro de los límites del cuadrante

### Generación de datos

Los datos se generan para cualquier dimensión con `generar_datos()`. Para trabajar siempre con los mismos datos se usa una seed de la librería `random`.

### Vecino más cercano

El vecino más cercano se encuentra con `encontrar_mas_cercano()`, que recibe el árbol y la coordenada con la que se va a comparar.

Este método primer mira que la raiz no esté subdividida y accede a la hoja que tenga, toma la distancia con el objetivo y retorna el par(punto, distancia)

Si está subdividida se recorre cada cuadrante hijo ordenados por la distancia calculada con `distancia_bordes()`. Esta función recibe el nodo y el objetivo, y calcula la distancia entre el dato que se busca y los bordes más cercanos del cuadrante. Se evalúa si esta distancia es menor a `mejor_distancia` para decidir si continuar la búsqueda en ese cuadrante, porque puede haber un dato más cercano. Esto es importante realizarlo porque pueden haber casos donde el dato que se busca esté muy cerca de algún borde y el dato más cercano esté al otro lado del borde.

Se recorre recursivamente todos los hijos que cumplan esta condición  hasta llegar a las hojas, se toman las distancias y se compara. Finalmente retorna el punto encontrado y la distancia

### Búsqueda por radio

La función para encontrar todos los valores dentro de un radio funciona de manera similar. Recibe:

- la raíz
- el centro del círculo
- el radio


Primero se crea la lista de encontrados vacía. Si el nodo no está subdividido y tiene una hoja, se mide la distancia entre la hoja y el objetivo, si es menor que el radio se añade a la lista.

Si está subdividido se hace algo similar a la búsqueda del vecino más cercano. Por cada hijo de la raiz se calcula la distancia usando `distancia_bordes()`, que retorna la distancia desde el objetivo hasta los bordes más cercanos del cuadrante. Se compara esta distancia con el radio y si es menor o igual al radio se hace la búsqueda recursiva en ese cuadrante y se van añadiendo las hojas que estén dentro del radio.

Finalmente se retorna la lista con todos las hojas encontradas

### Métodos de fuerza bruta

- `cercano_fuerza_bruta()` recorre la lista de datos buscando el dato objetivo y compara distancias guardando la menor.
- `radio_fuerza_bruta()` recorre la lista de datos, mide la distancia al centro y añade a una lista los puntos cuya distancia sea menor o igual al radio.

### Gráficas

Las funciones de graficar reciben los datos, el punto que se va a buscar, la raíz del árbol, los resultados y el radio para realizar los gráficos.

## 2. test.py
Este archivo som simplemente pruebas unitarias para verificar que los métodos funcionen, acompañados de los gráficos para visualizar los resultados y verificar que sean correctos

## 3. analisis.py
En este archivo se realizan las pruebas y mediciones de tiempo del arbol y los métodos de fuerza bruta con distintos tamaños de datos (ej: 1000, 5000, 10000, 50000, 100000). Por cada tamaño, se hacen 3 pruebas aleatorias, se mide el tiempo de cada una y se promedia. Estos datos se grafican en dos gráficos distintos, uno para el punto más cercano y otro para la búsqueda con radio. Estos gráficos tienen dos lineas que representan el tiempo que se demora el arbol y la fuerza bruta en función del tamaño de los datos.

# Análisis
Podemos ver en la gráfica de punto más cercano, entre más aumenta la cantidad de puntos, el tiempo de la fuerza bruta también se incrementa, mientras que el del árbol se mantiene casi que constante, casi de manera inmediata sin importar el tamaño de los datos.

Por otro lado, en la gráfica de la búsqueda por radio, podemos ver que al inicio, el Quadtree se demora menos en encontrar los datos que la fuerza bruta, pero a medida que aumenta el tamaño del radio, mientras que la fuerza bruta se mantiene relativamente constante, el árbol comienza a aumentar su tiempo hasta demorarse más que la fuerza bruta. Esto tiene la misma explicacion que el KDtree

Entre más grande sea el radio, el arbol debe bajar por más cuadrantes, por lo que pierde una de las caracteristicas que lo hacen eficiente, la cual es la "poda" o el descarte de las ramas, por lo tanto si el radio cubre casi la totalidad de los datos, el arbol debe bajar y volver a subir casi que por todos los nodos posibles, similar a la fuerza bruta, la diferencia es que el árbol hace llamadas recursivas y calcula diferencias en cada llamada, lo que aumenta mucho su tiempo a comparación de un simple recorrido de lista.


# Conclusión
Para encontrar el punto más cercano a un punto dado, es más eficiente usar un  sin importar el tamaño de los datos. Sin embargo, para encontrar los puntos dentro de un radio, los Quadtree  siguen siendo eficientes solo para radios que no cubran la totalidad de los datos, si el radio es demasiado grande es mejor hacer un recorrido de lista
