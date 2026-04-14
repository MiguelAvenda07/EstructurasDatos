# Laboratorio 2: Árboles KD

Código cocreado con ayuda de Claude.

Este laboratorio tiene 3 archivos.

## 1. KDtree.py

Este archivo contiene la clase `Nodo`, necesaria para crear los árboles. No hay una clase árbol como tal, pues este se crea tomando el nodo raíz y guardándolo en una variable. Como ese nodo ya está ligado a todo el árbol con los atributos `self.izquierdo` y `self.derecho`, consideré que no era necesario crear una clase entera cuyo único atributo fuera la raíz.

### Construcción del árbol

El árbol se construye con el método `construir()`, que recibe:

- una lista `datos` de parejas `(x, y)`
- una profundidad inicializada en `0`

Cuando la profundidad es `0`, cada pareja de la lista se convierte en un objeto `Nodo` y se agrega a una nueva lista llamada `puntos`; en otro caso, simplemente la lista `datos` se convierte en `puntos`.

El eje por el que se van a ordenar se define como el módulo de la profundidad dividida por las dimensiones del árbol. En un árbol 2D:

- si el módulo es `0`, se ordena por la coordenada `x`
- si es `1`, se ordena por la coordenada `y`

La raíz se toma como el valor medio (longitud de la lista dividida entre 2, redondeada hacia abajo). A partir de ahí, el hijo izquierdo y derecho se crean llamando la función de manera recursiva, enviando las dos mitades de la lista sin incluir la raíz y sumándole `1` a la profundidad para ordenar con la siguiente coordenada.

### Generación de datos

Los datos se generan para cualquier dimensión con `generar_datos()`. Para trabajar siempre con los mismos datos se usa una seed de la librería `random`.

### Vecino más cercano

El vecino más cercano se encuentra con `encontrar_mas_cercano()`, que recibe el árbol, la coordenada con la que se va a comparar y una profundidad inicializada en `0`.

El eje se define de la misma manera que en la construcción del árbol y el mejor candidato se inicia en la raíz. Si en el eje de la coordenada que se busca está más a la derecha que la de la raíz, se toma la rama derecha como la más cercana; si está más a la izquierda, se toma la rama izquierda.

Se baja primero por la rama más cercana usando recursión hasta el fondo, y luego se retorna comparando siempre el candidato con menor distancia. Cuando vuelve hacia arriba, se determina si vale la pena recorrer la rama más lejana comparando la distancia en el eje con el mejor candidato, ya que podría haber un punto más cercano allí. Al final, se retorna el mejor candidato.

### Búsqueda por radio

La función para encontrar todos los valores dentro de un radio funciona de manera similar. Recibe:

- la raíz
- el centro del círculo
- el radio
- profundidad inicializada en `0`
- la lista de encontrados inicializada en `None`

Primero se crea la lista y se mide la distancia de la raíz al centro del círculo. Si esa distancia es menor o igual al radio, el nodo está dentro del círculo y se añade a la lista de encontrados.

Luego se hace la misma clasificación de rama cercana y rama lejana según la distancia en el eje del centro respecto a la raíz. Como en la rama más lejana todavía puede haber puntos dentro del radio, si el valor absoluto de la distancia en el eje es menor al radio, también se recorre esa rama. Finalmente, se devuelve la lista de puntos encontrados.

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

Por otro lado, en la gráfica de la búsqueda por radio, podemos ver que al inicio, el árbol KD se demora menos en encontrar los datos que la fuerza bruta, pero a medida que aumenta el tamaño del radio, mientras que la fuerza bruta se mantiene relativamente constante, el árbol comienza a aumentar su tiempo hasta demorarse más que la fuerza bruta. Esto es interesante porque se supone que el árbol debería ser más eficiente que la fuerza bruta, pero de hecho tiene una explicación sencilla. 

Entre más grande sea el radio, el arbol debe bajar por más ramas, por lo que pierde una de las caracteristicas que lo hacen eficiente, la cual es la "poda" o el descarte de las ramas, por lo tanto si el radio cubre casi la totalidad de los datos, el arbol debe bajar y volver a subir casi que por todos los nodos posibles, similar a la fuerza bruta, la diferencia es que el árbol hace llamadas recursivas y calcula diferencias y valor absoluto en cada llamada, lo que aumenta mucho su tiempo a comparación de un simple recorrido de lista.

# Conclusión
Para encontrar el punto más cercano a un punto dado, es más eficiente usar un árbol KD sin importar el tamaño de los datos. Sin embargo, para encontrar los puntos dentro de un radio, los árboles KD siguen siendo eficientes solo para radios que no cubran la totalidad de los datos, si el radio es demasiado grande es mejor hacer un recorrido de lista
