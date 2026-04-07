import socket
from core.interface import glitch_msg, slow_type

class LookupModule:
    """
    O Oráculo - Módulo de Inteligência de Domínio e Footprinting.
    Mapeia a pegada digital externa através de resoluções DNS e Brute-force de nomes.
    """

    def __init__(self):
        # Opções de Contexto (Estado do Módulo)
        self.options = {
            "DOMAIN": "",             # Domínio alvo (ex: alvo.com)
            "WORDLIST": "common",     # common, small, deep (dicionários internos)
            "THREADS": "5",           # Intensidade de busca (simulada via timeout)
            "PROBE_IPV6": "ON",       # Tenta buscar registros AAAA
            "RECURSIVE": "OFF"        # Busca sub-subdomínios (ex: dev.api.alvo.com)
        }
        self.intel = {
            "ipv4": [],
            "ipv6": [],
            "subdomains": []
        }

    def enter_module(self):
        """Loop de interface interna do módulo Lookup."""
        glitch_msg("CONTEXTO: INTEL LOOKUP (THE ORACLE)")
        print("Digite 'set DOMAIN <alvo>' para começar ou 'run' para mapear.")
        
        while True:
            try:
                # Prompt de contexto Lookup (Azul Ciano)
                prompt = input("\n\033[1;37m(wired/\033[1;36mlookup\033[1;37m) \033[1;30m> \033[0m").strip().split()
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
                    if not self.options["DOMAIN"]:
                        print("\033[1;31m[!] Erro: DOMAIN não definido.\033[0m")
                        continue
                    self.execute_intel()

            except KeyboardInterrupt:
                print("\n[*] Retornando ao menu global...")
                break

    # --- LÓGICA DE INTELIGÊNCIA DNS ---

    def execute_intel(self):
        domain = self.options["DOMAIN"]
        self.intel = {"ipv4": [], "ipv6": [], "subdomains": []} # Reset

        slow_type(f"[*] Consultando registros base para {domain}...", speed=0.02)
        
        # 1. Resolução Base (A e AAAA)
        try:
            # IPv4
            ais = socket.getaddrinfo(domain, None, socket.AF_INET)
            self.intel["ipv4"] = list(set([addr[4][0] for addr in ais]))
            # IPv6
            if self.options["PROBE_IPV6"] == "ON":
                ais6 = socket.getaddrinfo(domain, None, socket.AF_INET6)
                self.intel["ipv6"] = list(set([addr[4][0] for addr in ais6]))
        except:
            print(f"[!] Falha na resolução base do domínio principal.")

        # 2. Subdomain Enumeration
        self._probe_subdomains(domain)

        # --- EXIBIÇÃO DO RELATÓRIO DE INTELIGÊNCIA ---
        print(f"\n\033[1;36m=== [ ORACLE INTEL REPORT: {domain} ] ===\033[0m")
        print(f" HOST PRINCIPAL | IPv4: {', '.join(self.intel['ipv4']) if self.intel['ipv4'] else 'N/A'}")
        if self.options["PROBE_IPV6"] == "ON":
            print(f" HOST PRINCIPAL | IPv6: {', '.join(self.intel['ipv6']) if self.intel['ipv6'] else 'N/A'}")
        
        if self.intel["subdomains"]:
            print(f"\n SUBDOMÍNIOS IDENTIFICADOS:")
            print(f" {'SUBDOMAIN':<25} | {'RESOLVED IP':<15}")
            print("-" * 45)
            for s in self.intel["subdomains"]:
                print(f" {s['host']:<25} | {s['ip']:<15}")
        else:
            print("\n [!] Nenhum subdomínio encontrado com a wordlist atual.")
        
        print("\033[1;36m" + "="*45 + "\033[0m")

    def _probe_subdomains(self, domain):
        """Sondagem de nomes baseada em dicionário interno."""
        # Wordlists internas baseadas na opção WORDLIST
        wordlists = {
            "common": ["www", "mail", "remote", "blog", "vpn", "api", "dev"],
            "small": ["www", "mail", "dev", "api", "staging", "test", "webmail", "ns1", "ns2"],
            "deep": ["www", "mail", "dev", "api", "staging", "test", "webmail", "ns1", "ns2", "ssh", "git", "mysql", "phpmyadmin", "cloud", "portal", "admin"]
        }
        
        targets = wordlists.get(self.options["WORDLIST"].lower(), wordlists["common"])
        print(f"[*] Iniciando enumeração ({len(targets)} alvos)...")

        for sub in targets:
            full_host = f"{sub}.{domain}"
            try:
                # Timeout implícito via socket default
                ip = socket.gethostbyname(full_host)
                self.intel["subdomains"].append({"host": full_host, "ip": ip})
                print(f"  \033[1;32m[+] Encontrado: {full_host} ({ip})\033[0m")
            except:
                continue

    # --- INTERFACE ---

    def _display_options(self):
        print(f"\n\033[1;37mVARIAVEIS DE CONFIGURAÇÃO (ORACLE/LOOKUP)\033[0m")
        print("-" * 55)
        for k, v in self.options.items():
            print(f"{k:15} | {v}")
        print("-" * 55)

    def _show_help(self):
        print("""
    COMANDOS LOOKUP:
    set <OPT> <VAL>  - Configura o domínio ou parâmetros de busca.
    show options     - Exibe a wordlist e o domínio atual.
    run              - Inicia a varredura DNS e subdomínios.
    back             - Retorna ao menu global (Wired).
    
    WORDLISTS (set WORDLIST <val>):
    common (7), small (9), deep (16)
        """)