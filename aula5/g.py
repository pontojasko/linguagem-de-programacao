import copy

lista1 = [1,2,3, [5, 60]]
lista_copia = copy.deepcopy(lista1)

del lista1[0]

print(id(lista1))
print(id(lista_copia))
print(lista1)
print(lista_copia)

# deleta