#string = "tenis pintado de branco e vermelho"



### acessar elementos

# print(string[4])

# print(len(string))

### printar letrinha por letrinha
# for elemento in string:
#     print(elemento)

### fatiamento de string sem parametro passo
# print(string[2:5:7])

### variavel string cheio de chamada de variavel

#reajuste = 10
#inflacao = 6.5

#frase = "o reajuste foi %d %% e a inflação foi de %.2f %%." % (reajuste, inflacao)
#print(frase)

### desabilitando comandos dentro da string do python com o r.
# print("instituto \\ federal")
# print(r"instituto \\ federal")

### concatenando strings
# só somar variavel com variavel igual

### comparando strings
#aluno1 = "heitor"
#aluno2 = "Heitor"

#if aluno1 == aluno2:
#    print("mesmo nome caralhoooo")
#else:
#    print("diferente estes nomes ham")
## comparando strings: python diferencia h de H
## caso compare com > ou < ele comparará usando as numerações da tabela ascii: na prática, é por ordem alfabética.

# procurando uma string em outra
s = "mario esta triste"
o = "mario"
ss = "     MUAHAHAHA     "

#if (o in s):
#    print(f"oi")
#else:
#    print(f"oii")

### formatacoes
print(s.upper())
print(ss.lower())
## retira espaco
print(ss.strip())
## replace
print(s.replace("mario esta", "eu estou"))
## e o split tira tudo q tive
    









