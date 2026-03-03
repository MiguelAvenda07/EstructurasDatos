with open("matriz.txt","w") as archivo:
    import time
    inicio = time.time()
    for i in range(100000):
        archivo.write("[ ")
        for j in range(3125):
            archivo.write("10101010101010101010101010101010")
        archivo.write(" ]\n")
    archivo.close()
    final = time.time()
    print(final - inicio)