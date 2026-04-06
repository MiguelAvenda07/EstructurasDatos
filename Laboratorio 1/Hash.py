import hashlib #Libreria para realizar los hashes

def encontrar_hash(hash_0):
    hash_i = "" #Se inicializa una cadena vacia
    cont = 0 #Contador para recorrer los numeros

    while hash_i != hash_0 or cont <= 9999999999: #Se recorre por fuerza bruta hasta que el hash sea igual o el numero tenga mas de 10 digitos
        cadena = ("0"*(10-len(str(cont)))) + str(cont) #Se genera una cadena de 10 digitos (condición del problema)
        hash_i = hashlib.sha256(cadena.encode()).hexdigest() #Se hace el hash 
        cont += 1

    if hash_i == "":
        return "No se encontró el hash"
    else:
        print("El número que genera el hash es: ", cadena)
    
cadena = input("Ingrese el hash que desea buscar: ")
print("Espere un momento por favor...")
encontrar_hash(cadena)

