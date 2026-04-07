# WIRED-FRAMEWORK
Framework modular de inteligência e auditoria de redes. Utiliza Scapy para pacotes RAW (SYN/Xmas), possui interface interativa estilo Metasploit (use module) e automação de workflow (binary mode). Oferece reconhecimento passivo, enumeração DNS e geração de relatórios técnicos em PDF.

---

# WIRED FRAMEWORK - MANUAL DE OPERAÇÃO
**Versão:** 3.0 (Elite Edition)
**Arquitetura:** Modular / Contextual (Console-Based)
**Linguagem:** Python 3.9+
**Requisito Crítico:** Privilégios de Administrador (ROOT/SUDO)

---

## 1. ESTRUTURA DO PROJETO
Para que o framework funcione, os arquivos devem estar organizados exatamente desta forma:

```
Wired_Project/
├── main.py              # Orquestrador Global e Modo Binary
├── requirements.txt     # Dependências (Scapy, FPDF2, Colorama)
├── core/
│   ├── __init__.py
│   ├── interface.py     # Banners e efeitos visuais
│   └── reporter.py      # Engine de geração de relatórios PDF
├── modules/
│   ├── __init__.py
│   ├── scanner.py       # Engine RAW (SYN/Xmas/OS Detection)
│   ├── ghost.py         # Recon Passivo / ARP Cache
│   ├── lookup.py        # Inteligência DNS / Subdomínios
│   └── surveyor.py      # Análise de Superfície / Hardening
└── relatorios/          # Pasta gerada automaticamente para os PDFs
```

---

## 2. INSTRUÇÕES DE INSTALAÇÃO

### Passo 1: Dependências do Sistema
No Linux (Debian/Ubuntu), certifique-se de ter as ferramentas de rede:
`sudo apt update && sudo apt install python3-pip -y`

### Passo 2: Dependências do Python
`pip install -r requirements.txt`

### Passo 3: Permissões de Raw Socket
O módulo `scanner` utiliza a biblioteca **Scapy** para forjar pacotes TCP. Isso requer acesso direto à placa de rede.
**Sempre execute como:** `sudo python3 main.py`

---

## 3. FLUXO DE TRABALHO (WORKFLOW)

O Wired Framework opera em dois modos principais:

### A. Modo Interativo (Manual)
Ideal para precisão e ajustes finos.
1. `show modules` -> Lista as ferramentas.
2. `use scanner` -> Entra no contexto do scanner.
3. `show options` -> Vê o que pode ser configurado (Target, Ports, Technique).
4. `set TARGET 1.1.1.1` -> Define o alvo.
5. `run` -> Inicia a operação.
6. `back` -> Retorna ao menu global para usar outro módulo.

### B. Modo Automático (Binary)
Ideal para reconhecimento rápido e geração de evidências.
1. No menu global: `binary google.com`
2. O sistema executará automaticamente:
   - Lookup (DNS/Subdomínios)
   - Scanner (SYN Scan T4)
   - Surveyor (Headers/Higiene)
3. Ao final, o sistema perguntará se deseja gerar o PDF.

---

## 4. DESCRIÇÃO DOS MÓDULOS

| Módulo | Função Principal | Técnica Utilizada |
| :--- | :--- | :--- |
| **Scanner** | Mapeamento de Portas | Stealth SYN Scan, Xmas, OS Detection via TTL. |
| **Ghost** | Vigilância Silenciosa | Leitura de Cache ARP e Tabelas de Rota (Passivo). |
| **Lookup** | Footprinting DNS | Brute-force de subdomínios e registros IPv4/v6. |
| **Surveyor** | Análise de Higiene | Banner Grabbing, Clock Drift e Security Headers. |

---

## 5. SOLUÇÃO DE PROBLEMAS (TROUBLESHOOTING)

* **Erro: "Permission Denied" ou "Operation not permitted"**
    * *Causa:* Tentativa de enviar pacotes RAW sem root.
    * *Solução:* Use `sudo python3 main.py`.
* **Erro: "Not enough horizontal space" no PDF**
    * *Causa:* O servidor enviou um banner gigante ou caracteres binários.
    * *Solução:* O arquivo `core/reporter.py` atualizado já limpa caracteres não-ASCII e usa `multi_cell`.
* **Módulos não encontrados (ImportError)**
    * *Causa:* Falta do arquivo `__init__.py` nas pastas `core` ou `modules`.
    * *Solução:* `touch core/__init__.py modules/__init__.py`.

---
**AVISO LEGAL:** Este software foi desenvolvido para fins de auditoria de segurança e testes de penetração autorizados. O uso contra alvos sem permissão explícita é ilegal.
---
