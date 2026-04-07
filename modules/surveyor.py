import socket
import time
import re
import email.utils
from core.interface import glitch_msg, slow_type

class SurveyorModule:
    """
    O Agrimensor - Módulo de Análise de Superfície e Higiene de Configuração.
    Disseca cabeçalhos, metadados de tempo e políticas de segurança (Hardening).
    """

    def __init__(self):
        # Opções de Contexto
        self.options = {
            "TARGET": "",        # IP ou Hostname
            "PORT": "80",        # Porta para análise (80, 8080, 443)
            "USER_AGENT": "Wired/3.0", # Identidade do probe
            "METHOD": "HEAD",    # HEAD, GET ou OPTIONS
            "INDUCT_ERROR": "ON" # Tenta forçar erro 405/500 para ver banners
        }
        self.report = {
            "web_tech": "Unknown",
            "admin_hygiene": "Unknown",
            "security_headers": {},
            "clock_drift": "0s"
        }

    def enter_module(self):
        """Loop de interface interna do módulo Surveyor."""
        glitch_msg("CONTEXTO: SURVEYOR (SURFACE ANALYSIS)")
        print("Digite 'set TARGET <alvo>' e 'run' para analisar a higiene do servidor.")
        
        while True:
            try:
                # Prompt de contexto Surveyor (Verde Água)
                prompt = input("\n\033[1;37m(wired/\033[1;36msurveyor\033[1;37m) \033[1;30m> \033[0m").strip().split()
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
                    self.execute_survey()

            except KeyboardInterrupt:
                print("\n[*] Retornando ao menu global...")
                break

    # --- LÓGICA DE ANÁLISE ---

    def execute_survey(self):
        target = self.options["TARGET"]
        port = int(self.options["PORT"])
        method = self.options["METHOD"].upper()
        
        slow_type(f"[*] Analisando superfície de {target}:{port}...", speed=0.02)
        
        # 1. Requisição de Cabeçalhos
        header_data = self._grab_header(target, port, method)
        
        if header_data:
            self._parse_http_intel(header_data)
            self._check_security_headers(header_data)
            self._calculate_drift(header_data)
            
            # 2. Indução de Erro (Opcional)
            if self.options["INDUCT_ERROR"] == "ON":
                self._probe_error_behavior(target, port)
                
            self._display_report()
        else:
            print(f"\033[1;31m[!] Falha crítica: O alvo não respondeu na porta {port}.\033[0m")

    def _grab_header(self, target, port, method):
        """Interação bruta via socket para capturar o banner HTTP."""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(3)
            sock.connect((target, port))
            
            payload = f"{method} / HTTP/1.1\r\n"
            payload += f"Host: {target}\r\n"
            payload += f"User-Agent: {self.options['USER_AGENT']}\r\n"
            payload += "Connection: close\r\n\r\n"
            
            sock.send(payload.encode())
            response = sock.recv(2048).decode(errors='ignore')
            sock.close()
            return response
        except:
            return None

    def _parse_http_intel(self, header):
        patterns = {
            "Server": r"Server: (.*)",
            "X-Powered-By": r"X-Powered-By: (.*)",
            "Backend": r"X-AspNet-Version: (.*)"
        }
        self.report["web_tech"] = "Custom/Cloaked"
        for tech, regex in patterns.items():
            match = re.search(regex, header, re.IGNORECASE)
            if match:
                self.report["web_tech"] = match.group(1).strip()

    def _probe_error_behavior(self, target, port):
        """Envia um método inexistente (BREW) para forçar o servidor a 'gritar' sua versão."""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            sock.connect((target, port))
            sock.send(b"BREW / HTTP/1.1\r\nHost: localhost\r\n\r\n")
            response = sock.recv(1024).decode(errors='ignore')
            
            if "Internal Server Error" in response or "405" in response:
                self.report["admin_hygiene"] = "\033[1;33mDEFAULT (Verbose Errors)\033[0m"
            else:
                self.report["admin_hygiene"] = "\033[1;32mSANITIZED (Custom Error Pages)\033[0m"
            sock.close()
        except:
            pass

    def _calculate_drift(self, header):
        match = re.search(r"Date: (.*) GMT", header)
        if match:
            try:
                srv_time = email.utils.parsedate_to_datetime(match.group(1) + " GMT").timestamp()
                drift = int(srv_time - time.time())
                self.report["clock_drift"] = f"{drift}s"
            except: pass

    def _check_security_headers(self, header):
        sec_headers = ["Content-Security-Policy", "X-Frame-Options", "Strict-Transport-Security", "X-Content-Type-Options"]
        for sh in sec_headers:
            status = "\033[1;32mPRESENT\033[0m" if sh.lower() in header.lower() else "\033[1;31mMISSING\033[0m"
            self.report["security_headers"][sh] = status

    # --- INTERFACE ---

    def _display_report(self):
        print(f"\n\033[1;36m=== [ SURVEYOR REPORT: {self.options['TARGET']} ] ===\033[0m")
        print(f" TECNOLOGIA BASE | {self.report['web_tech']}")
        print(f" HIGIENE ADMIN   | {self.report['admin_hygiene']}")
        print(f" CLOCK DRIFT     | {self.report['clock_drift']}")
        print(f"\n POLÍTICAS DE HARDENING (HEADERS):")
        for h, status in self.report["security_headers"].items():
            print(f"  > {h:28} | {status}")
        print("\033[1;36m" + "="*45 + "\033[0m")

    def _display_options(self):
        print(f"\n\033[1;37mVARIAVEIS DE CONFIGURAÇÃO (SURVEYOR)\033[0m")
        print("-" * 55)
        for k, v in self.options.items():
            print(f"{k:15} | {v}")
        print("-" * 55)

    def _show_help(self):
        print("""
    COMANDOS SURVEYOR:
    set <OPT> <VAL>  - Configura o alvo, porta ou método.
    show options     - Exibe as configurações atuais.
    run              - Analisa cabeçalhos e higiene do servidor.
    back             - Retorna ao menu global (Wired).
    
    TÉCNICAS:
    - Fingerprinting de Servidor (Banner Grabbing).
    - Hardening Check (Ausência de CSP, HSTS, etc).
    - Clock Drift (Detecta falha de sincronia/manutenção).
        """)