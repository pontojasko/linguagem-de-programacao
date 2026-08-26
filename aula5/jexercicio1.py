# calcular area total em metros de uma residencia
## insira nome, largura, comprimento do comodo.
### ai mostra o resultado da area.
#### perguntar se quer mais um comodo

print("calculator de area comodos legais ----")

i = "y"
while i == "y":
    nome = input("insira o nome: ")
    largura = float(input("insira a largura: "))
    comprimento = float(input("insira o comprimento: "))
    resultado = (largura * comprimento)
    print(f"seu comodo {nome} tem a area  {resultado}")
    i = input("quer mais? Y para sim e N para não: ")

print("obrigado por calcular .. ----")
    
    
