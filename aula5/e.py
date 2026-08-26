import copy

lista1 = [1,2,3, [5, 60]]
lista_copia = lista1.copy()

lista1[0] = 100

print(id(lista1))
print(id(lista_copia))
print(lista1)
print(lista_copia)

# aqui nao eh replica nao, copia mesmo