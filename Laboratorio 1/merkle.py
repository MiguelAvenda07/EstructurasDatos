import hashlib

def hash(value):
    return hashlib.sha256(value.encode()).hexdigest()

def build_merkle_tree(data): #Función para crear el arbol
    level = []
    for d in data:
        level.append(hash(d)) #Se añaden las transaciones al arbol
    
    while len(level) > 1:
        next_level = []
        for i in range(0, len(level)-1, 2):
            next_level.append(hash(level[i] + level[i+1])) #Se hacen los pares de hashes

        if len(level) % 2 != 0:
            next_level.append(level[-1]) #Se suben las transacciones sobrantes al siguiente nivel
            
        level = next_level
    
    return level #raiz del arbol

# Ejemplo
#trans = ["HOLA", "hola", "SI", "NO", "casa"]
#arbol = build_merkle_tree(trans)
#root = arbol[0] // 57f130820ca6826da41f75604c5e8558afa969dd3df3455fda77ba764b320581
#print(root)