resposta = int(input("Digite um numero: "))
tabuada = int(input("Digite o numero da tabuada (limite) "))
    
for resp in range(tabuada + 1):
    print(f"{resp} X {tabuada} = {resp * tabuada}")
    resp += 1
