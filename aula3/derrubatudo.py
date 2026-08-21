import threading
import requests
import time

alvo = "http://127.0.0.1:80/iisstart.htm"
threads_ativas = 800
requisicoes_por_thread = 900000000000000000000000000000

print(f"[*] Iniciando teste de carga no IIS ({alvo})...")
print(f"[*] Disparando {threads_ativas * requisicoes_por_thread} requisições simuladas.")

def atacar_iis():
    for _ in range(requisicoes_por_thread):
        try:
            # Envia a requisição para a página padrão encontrada
            resposta = requests.get(alvo, timeout=2)
            if resposta.status_code == 200:
                print("[+] Resposta 200: Servidor processando normalmente.")
        except requests.exceptions.RequestException:
            print("[!] O servidor falhou ou demorou demais para responder!")

lista_threads = []
tempo_inicio = time.time()

for i in range(threads_ativas):
    t = threading.Thread(target=atacar_iis)
    lista_threads.append(t)
    t.start()

for t in lista_threads:
    t.join()

print(f"\n[-] Teste finalizado em {time.time() - tempo_inicio:.2f} segundos.")
