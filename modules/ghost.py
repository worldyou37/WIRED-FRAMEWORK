import os
import re
import socket
import subprocess
from core.interface import glitch_msg, slow_type

class GhostModule:
    """
    O Espectro - Módulo de Reconhecimento Passivo e Monitoramento de Rede Local.
    Opera extraindo dados da cache do sistema e tabelas de roteamento.
    """

    def __init__(self):
        # Opções de Contexto (Estado do Módulo)
        self.options = {
            "INTERFACE": "auto",      # Interface de escuta (eth0, wlan0, etc)
            "VERBOSE": "ON",          # Exibição detalhada
            "DEEP_ARP": "OFF",        # Tenta forçar resolução ARP (Ativo)
            "LOG_FILE": "None"        # Salvar saída em arquivo
        }
        self.local_vitals = {
            "gateway": "Unknown",
            "local_ip": "Unknown",
            "neighbors": []
        }

    def enter_module(self):
        """Loop de interface interna do módulo Ghost."""
        glitch_msg("CONTEXTO: GHOST VIGILANCE (PASSIVE RECON)")
        print("Digite 'show options' para configurar ou 'run' para capturar espectro.")
        
        while True:
            try:
                # Prompt de contexto Ghost
                prompt = input("\n\033[1;37m(wired/\033[1;35mghost\033[1;37m) \033[1;30m> \033[0m").strip().split()
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
                    self.execute_vigilance()

            except KeyboardInterrupt:
                print("\n[*] Retornando ao menu global...")
                break

    # --- LÓGICA DE INTELIGÊNCIA ---

    def execute_vigilance(self):
        """Orquestra a coleta de dados passivos."""
        slow_type("[*] Sincronizando com a memória do sistema...", speed=0.02)
        
        # 1. Identificar Identidade Local
        self._identify_local_identity()
        
        # 2. Ler Tabela ARP
        self._read_arp_cache()
        
        # 3. Checar IPv6
        ipv6_status = self._check_ipv6_presence()

        # --- EXIBIÇÃO DO RELATÓRIO GHOST ---
        print("\n\033[1;35m=== [ GHOST VIGILANCE REPORT ] ===\033[0m")
        print(f" IDENTIDADE  | IP: {self.local_vitals['local_ip']} | GW: {self.local_vitals['gateway']}")
        print(f" IPV6 STATUS | {ipv6_status}")
        
        if self.local_vitals["neighbors"]:
            print(f"\n VIZINHOS DETECTADOS NA CACHE ARP:")
            print(f" {'IP ADDRESS':<18} | {'MAC ADDRESS':<18}")
            print("-" * 40)
            for n in self.local_vitals["neighbors"]:
                print(f" {n['ip']:<18} | {n['mac']:<18}")
        else:
            print("\n [!] Nenhuma entrada encontrada na cache ARP (Rede Isolada).")
        
        print("\033[1;35m" + "="*34 + "\033[0m")

    def _identify_local_identity(self):
        """Detecta IP local e Gateway padrão sem pacotes externos."""
        try:
            # Pega IP local
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            self.local_vitals["local_ip"] = s.getsockname()[0]
            s.close()
            
            # Tenta deduzir Gateway (Simplificado para o contexto)
            base_ip = ".".join(self.local_vitals["local_ip"].split(".")[:-1])
            self.local_vitals["gateway"] = f"{base_ip}.1"
        except:
            self.local_vitals["local_ip"] = "127.0.0.1"

    def _read_arp_cache(self):
        """Extrai dispositivos vizinhos da tabela ARP do OS."""
        self.local_vitals["neighbors"] = []
        try:
            # Comando multiplataforma (ajustado para Linux/Unix)
            output = subprocess.check_output(["arp", "-n"]).decode(errors='ignore')
            
            # Regex para capturar IP e MAC
            # Padrão típico: 192.168.1.10 ether 00:11:22:33:44:55
            neighbors = re.findall(r"(\d+\.\d+\.\d+\.\d+)\s+.*?\s+([0-9a-fA-F:]{17})", output)
            
            for ip, mac in neighbors:
                if mac != "00:00:00:00:00:00":
                    self.local_vitals["neighbors"].append({"ip": ip, "mac": mac})
        except:
            pass

    def _check_ipv6_presence(self):
        """Verifica suporte a IPv6 (Canais de comunicação silenciosos)."""
        try:
            output = subprocess.check_output(["ip", "-6", "addr", "show"]).decode()
            if "global" in output.lower():
                return "\033[1;32mATIVO (Global detectado)\033[0m"
            return "Apenas Local (Link-local)"
        except:
            return "Desativado/Não suportado"

    # --- INTERFACE ---

    def _display_options(self):
        print(f"\n\033[1;37mVARIAVEIS DE CONFIGURAÇÃO (GHOST)\033[0m")
        print("-" * 55)
        for k, v in self.options.items():
            print(f"{k:15} | {v}")
        print("-" * 55)

    def _show_help(self):
        print("""
    COMANDOS GHOST:
    set <OPT> <VAL>  - Configura variáveis do espectro.
    show options     - Exibe as configurações atuais.
    run              - Inicia a coleta de inteligência passiva.
    back             - Retorna ao menu global (Wired).
    
    DESCRIÇÃO:
    O Ghost não envia pacotes de varredura. Ele analisa o que o seu
    computador já 'ouviu' na rede para evitar detecção por IDS/IPS.
        """)