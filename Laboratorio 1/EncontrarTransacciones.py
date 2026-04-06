def encontrar_transacciones(root, transacciones):
    import itertools
    from merkle import build_merkle_tree
    combinaciones = list(itertools.permutations(transacciones)) #Se hacen las combinaciones posibles de las transacciones 
    for i in combinaciones:
        arbol = build_merkle_tree(i) 
        if arbol[0] == root: #Por cada combinacion posible se hace el arbol y se compara la raiz con la ingresada
            return i 
    return ("No se encontraron las transacciones que generan el hash raíz")

transacciones = []
cant = int(input("Ingrese cuantas transacciones va a realizar: "))

for i in range(cant):
    transaccion = input("Ingrese la transacción: ")
    transacciones.append(transaccion)
root = input("Ingrese la root del arbol: ")
    
print("Orden que genera la root: ", encontrar_transacciones(root, transacciones))