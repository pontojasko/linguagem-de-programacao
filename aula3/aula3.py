quadrado = 0
faixa = 15
faixa1 = 200

while faixa != faixa1: ## enquanto o 15 for diferente de 200 ele entra
    quadrado = faixa * faixa ## faixa * faixa (15 x 15) = 225
    print("Num:" , faixa , "Resp" ,quadrado) ## mostra ao usuário
    faixa += 1 ## acrescenta no contador para saber que deu 200 ou 201
    