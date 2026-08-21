N = 5
notas = []
media = 0

print("digite")

for i in range(N):
    x = float(input(f"nota do aluno {i+1}:"))
    notas.append(x)
    media = media + x

media = media / N
for x in notas:
    if x > media:
        print(x)