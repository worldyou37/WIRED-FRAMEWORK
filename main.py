import sys
import os

# --- IMPORTAÇÃO DA INTERFACE E UTILITÁRIOS ---
from core.interface import show_banner, clear_screen, glitch_msg, slow_type
from core.reporter import IntelligenceReporter

# --- IMPORTAÇÃO DOS MÓDULOS DE CONTEXTO ---
from modules.scanner import ScannerModule
from modules.ghost import GhostModule
from modules.lookup import LookupModule
from modules.surveyor import SurveyorModule

class WiredFramework:
    def __init__(self):
        # Instanciação dos módulos para persistência de dados
        self.modules = {
            "scanner": ScannerModule(),
            "ghost": GhostModule(),
            "lookup": LookupModule(),
            "surveyor": SurveyorModule()
        }
        self.current_module = None

    def run(self):
        """Loop principal do Framework."""
        clear_screen()
        show_banner()
        slow_type(" [!] Sistema de Inteligência Wired v3.0 carregado.", speed=0.01)
        print(" [i] Digite 'show modules' para listar ou 'use <nome>' para entrar.")
        
        while True:
            try:
                # Prompt Global (Cinza/Branco)
                prompt_text = "\n\033[1;37m(wired) \033[1;30m> \033[0m"
                user_input = input(prompt_text).strip().split()
                
                if not user_input: continue
                
                cmd = user_input[0].lower()
                args = user_input[1:]

                # --- LÓGICA DE COMANDOS GLOBAIS ---
                if cmd in ["exit", "quit"]:
                    glitch_msg("Encerrando sessões de inteligência. Adeus.")
                    break

                elif cmd == "help":
                    self._global_help()

                elif cmd == "clear":
                    clear_screen()
                    show_banner()

                elif cmd == "show" and args and args[0] == "modules":
                    print("\n\033[1;37mSERVIÇOS DISPONÍVEIS NO KERNEL:\033[0m")
                    print("-" * 35)
                    for m in self.modules.keys():
                        desc = self._get_module_desc(m)
                        print(f"  \033[1;32m{m:<10}\033[0m | {desc}")

                elif cmd == "use" and args:
                    mod_name = args[0].lower()
                    if mod_name in self.modules:
                        # ENTRADA NO CONTEXTO DO MÓDULO
                        self.modules[mod_name].enter_module()
                    else:
                        print(f"\033[1;31m[!] Erro: Módulo '{mod_name}' não indexado.\033[0m")

                # --- COMANDO AUTOMATIZADO: BINARY ---
                elif cmd == "binary" and args:
                    self._execute_binary_workflow(args[0])

                else:
                    print(f"[?] Comando '{cmd}' desconhecido no nível global.")

            except KeyboardInterrupt:
                print("\n[!] Use 'exit' para fechar o framework.")
            except Exception as e:
                print(f"\n[X] Erro de Kernel: {e}")

    # --- MÉTODOS DE APOIO ---

    def _get_module_desc(self, name):
        descriptions = {
            "scanner": "Varredura RAW (SYN/Xmas/OS Detection)",
            "ghost": "Reconhecimento Passivo e Cache ARP",
            "lookup": "Inteligência DNS e Subdomínios",
            "surveyor": "Análise de Cabeçalhos e Higiene Admin"
        }
        return descriptions.get(name, "Módulo de operação.")

    def _execute_binary_workflow(self, target):
        """
        MODO BINARY: Orquestra todos os módulos em sequência rápida 
        e gera o relatório PDF profissional ao final.
        """
        glitch_msg(f"MODO BINÁRIO: COMPILANDO RELATÓRIO DE AGÊNCIA PARA {target}")
        
        # 1. Reconhecimento DNS (Lookup)
        lookup = self.modules["lookup"]
        lookup.options["DOMAIN"] = target
        lookup.execute_intel() # Coleta IPv4, IPv6 e Subdomínios

        # 2. Varredura de Portas (Scanner)
        scanner = self.modules["scanner"]
        scanner.options["TARGET"] = target
        scanner.options["TECHNIQUE"] = "SYN"
        scanner.options["TIMING"] = "4"
        scanner.execute_scan() # Varre portas padrão

        # 3. Análise de Superfície (Surveyor)
        surveyor = self.modules["surveyor"]
        surveyor.options["TARGET"] = target
        surveyor.execute_survey() # Checa headers e tecnologia

        # --- GERAÇÃO DO PDF ---
        print("\n" + "="*50)
        opt = input("[?] Deseja exportar o relatório PDF de inteligência? (s/n): ").lower()
        if opt == 's':
            slow_type("[*] Assinando documento com chaves criptográficas...", 0.03)
            reporter = IntelligenceReporter()
            
            # Estrutura os dados coletados de cada módulo
            report_data = [
                {"title": "DNS Intelligence & Footprinting", "content": lookup.intel},
                {"title": "Active Recon (Stealth Scan)", "content": scanner.last_results},
                {"title": "Infrastructure Hygiene & Headers", "content": surveyor.report}
            ]
            
            path = reporter.generate_intel_report(target, report_data)
            print(f"\n\033[1;32m[+] OPERAÇÃO CONCLUÍDA. RELATÓRIO GERADO: {path}\033[0m")
        else:
            print("[*] Dados descartados da memória volátil.")

    def _global_help(self):
        print("""
    COMANDOS GLOBAIS:
    ---------------------------------------------------------
    show modules        - Lista todos os módulos carregados.
    use <module>        - Entra no modo de configuração do módulo.
    binary <target>     - Varredura automatizada completa + PDF.
    clear               - Limpa o terminal.
    exit                - Encerra o Wired Framework.
    ---------------------------------------------------------
        """)

if __name__ == "__main__":
    # Verificação de privilégios ROOT (Necessário para Scapy)
    if os.geteuid() != 0:
        print("\033[1;31m[!] ERRO: O Framework requer privilégios de ROOT para pacotes RAW.\033[0m")
        print("Tente: sudo python3 main.py")
        sys.exit(1)
        
    WiredFramework().run()