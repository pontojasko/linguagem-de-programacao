import ipaddress
import subprocess
import concurrent.futures
import socket
import re
import sys


# ============================================================
# CONFIGURAÇÃO
# ============================================================

PING_TIMEOUT = 2             # 2 segundos por IP
MAX_WORKERS = 10000             # IPs testados simultaneamente

TEMPO_SHUTDOWN = 5
MENSAGEM = "Sistemas em manutenção"


# ============================================================
# DETECTAR REDE AUTOMATICAMENTE
# ============================================================

def obter_rede_local():

    try:
        # Descobre o IP da interface utilizada para acessar a rede.
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.connect(("8.8.8.8", 80))

        ip_local = sock.getsockname()[0]

        sock.close()

    except Exception:

        ip_local = socket.gethostbyname(
            socket.gethostname()
        )

    resultado = subprocess.run(
        ["ipconfig"],
        capture_output=True,
        text=True,
        encoding="cp850",
        errors="ignore"
    )

    linhas = resultado.stdout.splitlines()

    mascara = None

    for i, linha in enumerate(linhas):

        if ip_local in linha:

            for proxima in linhas[i:i + 10]:

                match = re.search(
                    r"(?:Máscara de Sub-rede|Subnet Mask).*?:\s*([\d.]+)",
                    proxima,
                    re.IGNORECASE
                )

                if match:
                    mascara = match.group(1)
                    break

            if mascara:
                break

    if not mascara:
        raise RuntimeError(
            "Não foi possível identificar a máscara da rede."
        )

    rede = ipaddress.IPv4Network(
        f"{ip_local}/{mascara}",
        strict=False
    )

    return ip_local, mascara, rede


# ============================================================
# TESTAR UM IP
# ============================================================

def testar_ip(ip):

    try:

        resultado = subprocess.run(
            [
                "ping",
                "-n", "1",
                "-w", str(PING_TIMEOUT * 1000),
                str(ip)
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,

            # Timeout TOTAL do processo.
            timeout=PING_TIMEOUT + 1
        )

        if resultado.returncode == 0:
            return str(ip), "ONLINE"

        return str(ip), "TIMEOUT"

    except subprocess.TimeoutExpired:

        return str(ip), "TIMEOUT"

    except Exception as erro:

        return str(ip), f"ERRO: {erro}"


# ============================================================
# DESCOBRIR COMPUTADORES
# ============================================================

def descobrir_hosts(rede, ip_local):

    hosts = [
        str(ip)
        for ip in rede.hosts()
        if str(ip) != ip_local
    ]

    total = len(hosts)

    print("\n" + "=" * 70)
    print(" INICIANDO VARREDURA")
    print("=" * 70)

    print(f"\nTotal de IPs para verificar: {total}")
    print(f"Timeout por IP: {PING_TIMEOUT} segundos")
    print(f"Processos simultâneos: {MAX_WORKERS}\n")

    encontrados = []

    contador = 0

    with concurrent.futures.ThreadPoolExecutor(
        max_workers=MAX_WORKERS
    ) as executor:

        tarefas = {
            executor.submit(testar_ip, ip): ip
            for ip in hosts
        }

        for tarefa in concurrent.futures.as_completed(tarefas):

            contador += 1

            ip, resultado = tarefa.result()

            if resultado == "ONLINE":

                encontrados.append(ip)

                print(
                    f"[{contador:05d}/{total:05d}] "
                    f"{ip:<15} -> ONLINE"
                )

            elif resultado == "TIMEOUT":

                print(
                    f"[{contador:05d}/{total:05d}] "
                    f"{ip:<15} -> TIMEOUT"
                )

            else:

                print(
                    f"[{contador:05d}/{total:05d}] "
                    f"{ip:<15} -> {resultado}"
                )

    return sorted(
        encontrados,
        key=lambda x: ipaddress.IPv4Address(x)
    )


# ============================================================
# DESLIGAR COMPUTADOR
# ============================================================

def desligar(ip):

    comando = [
        "shutdown",
        "/m", f"\\\\{ip}",
        "/s",
        "/t", str(TEMPO_SHUTDOWN),
        "/c", MENSAGEM
    ]

    try:

        resultado = subprocess.run(
            comando,
            capture_output=True,
            text=True,
            encoding="cp850",
            errors="ignore",

            # Timeout para o comando remoto.
            timeout=10
        )

        if resultado.returncode == 0:

            return True, "Comando aceito"

        erro = (
            resultado.stderr.strip()
            or resultado.stdout.strip()
            or "Erro desconhecido"
        )

        return False, erro

    except subprocess.TimeoutExpired:

        return False, "TIMEOUT"

    except Exception as erro:

        return False, str(erro)


# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 70)
    print("        SHUTDOWN REMOTO - REDE AUTOMÁTICA")
    print("=" * 70)

    # --------------------------------------------------------
    # DETECTAR REDE
    # --------------------------------------------------------

    try:

        ip_local, mascara, rede = obter_rede_local()

        print("\n[+] Rede detectada automaticamente")
        print(f"[+] IP deste computador : {ip_local}")
        print(f"[+] Máscara             : {mascara}")
        print(f"[+] Sub-rede            : {rede}")

    except Exception as erro:

        print(f"\n[ERRO] {erro}")
        sys.exit(1)

    # --------------------------------------------------------
    # DESCOBRIR COMPUTADORES
    # --------------------------------------------------------

    hosts = descobrir_hosts(
        rede,
        ip_local
    )

    print("\n" + "=" * 70)
    print(" COMPUTADORES ONLINE")
    print("=" * 70)

    if not hosts:

        print("\n[NENHUM] Nenhum computador respondeu ao ping.")
        return

    for ip in hosts:

        print(f"  [ONLINE] {ip}")

    print(
        f"\nTotal de computadores encontrados: {len(hosts)}"
    )

    # --------------------------------------------------------
    # CONFIRMAÇÃO
    # --------------------------------------------------------

    print("\n" + "=" * 70)
    print(" ATENÇÃO")
    print("=" * 70)

    print(
        f"\nSerão enviados comandos de desligamento "
        f"para {len(hosts)} computador(es)."
    )

    print(f"Mensagem: {MENSAGEM}")
    print(f"Tempo para desligar: {TEMPO_SHUTDOWN} segundos")

    print(
        f"\nO computador local ({ip_local}) "
        "NÃO será desligado."
    )

    confirmacao = input(
        '\nDigite "DESLIGAR" para continuar: '
    ).strip()

    if confirmacao != "DESLIGAR":

        print(
            "\n[ABORTADO] Nenhum comando foi enviado."
        )

        return

    # --------------------------------------------------------
    # SHUTDOWN
    # --------------------------------------------------------

    print("\n" + "=" * 70)
    print(" ENVIANDO SHUTDOWN")
    print("=" * 70)

    sucesso = []
    falha = []

    for ip in hosts:

        print(
            f"\n[... ] {ip}",
            end=" ",
            flush=True
        )

        ok, mensagem = desligar(ip)

        if ok:

            print(
                f"-> SUCESSO ({mensagem})"
            )

            sucesso.append(ip)

        else:

            print(
                f"-> FALHA ({mensagem})"
            )

            falha.append(
                (ip, mensagem)
            )

    # --------------------------------------------------------
    # RESULTADO
    # --------------------------------------------------------

    print("\n" + "=" * 70)
    print(" RESULTADO FINAL")
    print("=" * 70)

    print(
        f"\nSUCESSO: {len(sucesso)}"
    )

    for ip in sucesso:

        print(
            f"  [OK]    {ip}"
        )

    print(
        f"\nFALHA: {len(falha)}"
    )

    for ip, motivo in falha:

        print(
            f"  [ERRO]  {ip} -> {motivo}"
        )

    print("\n" + "=" * 70)
    print(" FIM")
    print("=" * 70)


if __name__ == "__main__":
    main()