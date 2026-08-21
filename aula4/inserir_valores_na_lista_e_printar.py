# criar uma lista c 8 posições
# solicitar ao usuario para digitar os valores
# exibir os valores da lista
# exibir o tamanho da lista
# calcular a media dos valores digitados da lista
# calcular a potencia de cada elemento da lista e escrever o resultado como   eleemnto / valores da potencia


valores = []
print("digite os valores")
for i in range(8):
    x = float(input(f"valores {i + 1}: "))
    # ok ate aqui ele ta pedindo os 8 valores e pedindo o próximo

    # o append coloca no final da lista o valor, nesse caso, cada vez q o usuario coloca o valor ele poe esse valor no final da lista
    valores.append(x)

print(valores)