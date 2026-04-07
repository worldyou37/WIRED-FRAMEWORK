import json
import os
from core.interface import slow_type, glitch_msg

class ProfileManager:
    """
    O Arquiteto - Gestor e Construtor de Perfis de Missão.
    Permite criar, salvar e carregar configurações personalizadas.
    """

    def __init__(self, storage_path="templates/"):
        self.storage_path = storage_path
        if not os.path.exists(storage_path):
            try:
                os.makedirs(storage_path)
            except: pass
        
        # Perfis imutáveis do sistema
        self.system_defaults = ["stealth_recon", "full_audit"]

    def create_interactive_template(self):
        """Assistente interativo para criar um template .json."""
        print("\n\033[1;36m--- [ CONFIGURADOR DE TEMPLATE ] ---\033[0m")
        name = input("[?] Nome do novo perfil: ").strip().lower()
        if not name: return

        # Estrutura base do template
        config = {
            "scanner": {"ports": "80,443", "aggression": 2},
            "lookup": {"subdomains": True},
            "surveyor": {"active": True},
            "ghost": {"active": True}
        }

        # Configuração do Scanner
        print("\n\033[1;30m> Configurando Scanner Ativo:\033[0m")
        config["scanner"]["ports"] = input("  Range de Portas (ex: 1-1024, 8080): ") or "80,443"
        try:
            config["scanner"]["aggression"] = int(input("  Nível de Agressividade (1-3): ") or 2)
        except: config["scanner"]["aggression"] = 2

        # Configuração do Lookup
        print("\n\033[1;30m> Configurando DNS Intel:\033[0m")
        sub = input("  Ativar busca de subdomínios? (s/n): ").lower()
        config["lookup"]["subdomains"] = True if sub == 's' else False

        # Configuração do Surveyor
        print("\n\033[1;30m> Configurando Surveyor:\033[0m")
        srv = input("  Ativar análise de cabeçalhos/higiene? (s/n): ").lower()
        config["surveyor"]["active"] = True if srv == 's' else False

        # Salvando
        if self.save_template(name, config):
            glitch_msg(f"Template '{name}' forjado com sucesso em {self.storage_path}")
        
    def save_template(self, name, config):
        file_path = os.path.join(self.storage_path, f"{name}.json")
        try:
            with open(file_path, 'w') as f:
                json.dump(config, f, indent=4)
            return True
        except Exception as e:
            print(f"[!] Erro ao gravar arquivo: {e}")
            return False

    def load_template(self, name):
        """Carrega do disco ou retorna configurações de sistema."""
        file_path = os.path.join(self.storage_path, f"{name}.json")
        
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r') as f:
                    return json.load(f)
            except: return None
        
        # Fallback para defaults
        if name == "stealth_recon":
            return {"scanner": {"ports": "80,443,22", "aggression": 1}, "lookup": {"subdomains": False}, "surveyor": {"active": True}}
        if name == "full_audit":
            return {"scanner": {"ports": "1-65535", "aggression": 3}, "lookup": {"subdomains": True}, "surveyor": {"active": True}}
        
        return None

    def list_templates(self):
        """Lista arquivos físicos e padrões do sistema."""
        try:
            files = [f.replace('.json', '') for f in os.listdir(self.storage_path) if f.endswith('.json')]
        except:
            files = []
        return list(set(self.system_defaults + files))