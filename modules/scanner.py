import time
import random
import ipaddress
from scapy.all import IP, TCP, sr1, sr, RandShort, Raw, conf
from core.interface import glitch_msg, slow_type

# Silencia avisos desnecessários da Scapy
conf.verb = 0

class ScannerModule:
    def __init__(self):
        # Dicionário de Opções (Contexto do Módulo)
        self.options = {
            "TARGET": "",           # IP, CIDR ou Hostname
            "PORTS": "21,22,80,443", # Lista ou Range (1-1024)
            "TECHNIQUE": "SYN",      # SYN, CONNECT, NULL, FIN, XMAS
            "TIMING": "3",           # T0 a T5
            "OS_PROBE": "OFF",       # ON/OFF
            "DECOY": "None",         # IP1,IP2...
            "SPOOF": "None",         # Source IP Spoofing
            "DATA_LEN": "0"          # Random data padding
        }
        self.last_results = {}

    def enter_module(self):
        """Loop de interface interna do módulo."""
        glitch_msg("CONTEXTO: OMNI-SCANNER ATIVADO")
        print("Digite 'show options' para configurar ou 'help' para comandos.")
        
        while True:
            try:
                # Prompt de contexto específico
                prompt = input("\n\033[1;37m(wired/\033[1;32mscanner\033[1;37m) \033[1;30m> \033[0m").strip().split()
                if not prompt: continue
                
                cmd = prompt[0].lower()
                args = prompt[1:]

                if cmd == "back":
                    break
                
                elif cmd == "help":
                    self._show_help()

                elif cmd == "show" and args and args[0] == "options":
                    self._display_options()

                elif cmd == "set" and len(args) >= 2:
                    key = args[0].upper()
                    val = " ".join(args[1:])
                    if key in self.options:
                        self.options[key] = val
                        print(f"[*] {key} => {val}")
                    else:
                        print(f"[!] Opção '{key}' desconhecida.")

                elif cmd == "run":
                    if not self.options["TARGET"]:
                        print("\033[1;31m[!] Erro: TARGET não definido.\033[0m")
                        continue
                    self.execute_scan()

            except KeyboardInterrupt:
                print("\n[*] Retornando...")
                break

    # --- LÓGICA DE EXECUÇÃO (SCAPY ENGINE) ---

    def execute_scan(self):
        target = self.options["TARGET"]
        ports = self._parse_ports(self.options["PORTS"])
        tech = self.options["TECHNIQUE"].upper()
        timing = int(self.options["TIMING"])
        
        slow_type(f"[*] Iniciando sequência {tech} em {target}...", speed=0.02)
        
        # Gerenciamento de Timing (Atraso entre pacotes)
        delays = {0: 5, 1: 2, 2: 0.5, 3: 0.1, 4: 0.01, 5: 0}
        delay = delays.get(timing, 0.1)

        found_ports = {}

        for port in ports:
            # Lógica de Evasão (Padding de Dados)
            data_padding = Raw(load=random._urandom(int(self.options["DATA_LEN"]))) if int(self.options["DATA_LEN"]) > 0 else ""
            
            # Montagem do Pacote Base
            ip_pkt = IP(dst=target)
            if self.options["SPOOF"] != "None":
                ip_pkt.src = self.options["SPOOF"]

            # Seleção de Técnica
            if tech == "SYN":
                tcp_pkt = TCP(sport=RandShort(), dport=port, flags="S")
                ans = sr1(ip_pkt/tcp_pkt/data_padding, timeout=1, verbose=0)
                
                if ans and ans.haslayer(TCP):
                    if ans.getlayer(TCP).flags == 0x12: # SYN-ACK
                        # Envia RST para fechar silenciosamente
                        sr(IP(dst=target)/TCP(sport=tcp_pkt.sport, dport=port, flags="R"), timeout=1, verbose=0)
                        found_ports[port] = "OPEN"
                        print(f"  \033[1;32m[+] Porta {port}: ABERTA (SYN-ACK)\033[0m")
            
            elif tech == "XMAS":
                tcp_pkt = TCP(sport=RandShort(), dport=port, flags="FPU")
                ans = sr1(ip_pkt/tcp_pkt/data_padding, timeout=1, verbose=0)
                if ans is None:
                    found_ports[port] = "OPEN|FILTERED"
                    print(f"  \033[1;33m[!] Porta {port}: OPEN|FILTERED (No response)\033[0m")

            time.sleep(delay)

        # OS Detection (Heurística de TTL)
        if self.options["OS_PROBE"] == "ON":
            self._probe_os(target)

        self.last_results = found_ports
        print(f"\n[*] Varredura em {target} finalizada.")

    # --- MÉTODOS AUXILIARES ---

    def _display_options(self):
        print(f"\n\033[1;37mVARIAVEIS DE CONFIGURAÇÃO (SCANNER)\033[0m")
        print("-" * 55)
        for k, v in self.options.items():
            print(f"{k:15} | {v}")
        print("-" * 55)

    def _parse_ports(self, port_str):
        if "-" in port_str:
            s, e = map(int, port_str.split("-"))
            return list(range(s, e + 1))
        return [int(p) for p in port_str.split(",")]

    def _probe_os(self, target):
        pkt = IP(dst=target)/TCP(dport=80, flags="S")
        ans = sr1(pkt, timeout=1, verbose=0)
        if ans:
            ttl = ans.getlayer(IP).ttl
            os_type = "Linux/Unix" if ttl <= 64 else "Windows" if ttl <= 128 else "Network Device"
            print(f"[*] OS Detection: \033[1;36m{os_type}\033[0m (TTL: {ttl})")

    def _show_help(self):
        print("""
    COMANDOS:
    set <OPT> <VAL>  - Define o valor de uma variável.
    show options     - Exibe a tabela de configuração atual.
    run              - Dispara o scanner com as opções atuais.
    back             - Retorna ao menu global.
    
    TÉCNICAS DISPONÍVEIS (set TECHNIQUE <VAL>):
    SYN, CONNECT, NULL, FIN, XMAS
        """)