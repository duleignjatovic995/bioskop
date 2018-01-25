lista = [1,2,3,4,5,6,7,8,9]

def metoda():
    for l in lista:
        if l % 2 == 0:
            lista.remove(l)

metoda()
print(lista)