import re

class DataTranslator:
    """
    O Intérprete - Decifra os ecos da 'Wired'.
    Transforma banners brutos e metadados em inteligência legível.
    """

    @staticmethod
    def identify_service(port, banner):
        """
        Mapeamento de portas e assinaturas de serviço.
        """
        # Base de serviços comuns por porta
        port_map = {
            21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP", 53: "DNS",
            80: "HTTP", 110: "POP3", 139: "NetBIOS", 443: "HTTPS", 
            445: "Microsoft-DS", 3306: "MySQL", 3389: "RDP", 5432: "PostgreSQL",
            8080: "HTTP-Proxy", 27017: "MongoDB"
        }

        service = port_map.get(port, "Unknown Service")

        # Refinamento por análise de banner
        if banner:
            banner_lower = banner.lower()
            if "apache" in banner_lower: service = "Apache Web Server"
            elif "nginx" in banner_lower: service = "Nginx Web Server"
            elif "openssh" in banner_lower: service = "OpenSSH"
            elif "microsoft-iis" in banner_lower: service = "IIS"
            elif "postfix" in banner_lower: service = "Postfix SMTP"
            elif "mysql" in banner_lower: service = "MySQL DB"
            
        return service

    @staticmethod
    def analyze_vulnerability(banner):
        """
        Heurística de vulnerabilidades baseada em strings de versão.
        Focado em identificar softwares obsoletos ou críticos.
        """
        if not banner:
            return "No signature"

        critical_flags = {
            r"OpenSSH_7.2": "CVE-2016-6210 (User Enumeration)",
            r"Apache/2.4.18": "Outdated Version (Multiple CVEs)",
            r"PHP/5.": "PHP 5.x EOL (High Risk)",
            r"IIS/7.5": "Legacy Windows Server (End of Support)",
            r"smbd [3-4].": "Samba (Check for IPC$ access)",
            r"vsFTPd 2.3.4": "Potential Backdoor (CVE-2011-2523)"
        }

        found_vulns = []
        for pattern, note in critical_flags.items():
            if re.search(pattern, banner, re.IGNORECASE):
                found_vulns.append(note)

        return found_vulns if found_vulns else "Identified (No critical flags)"

    @staticmethod
    def infer_os(rtt, banner):
        """
        Inferência de SO por comportamento de rede e pistas no banner.
        """
        # Prioridade 1: Pistas explícitas no banner
        if banner:
            if "ubuntu" in banner.lower() or "debian" in banner.lower():
                return "Linux (Debian-based)"
            if "win32" in banner.lower() or "microsoft" in banner.lower():
                return "Windows Server Family"
            if "centos" in banner.lower() or "redhat" in banner.lower():
                return "Linux (RHEL-based)"

        # Prioridade 2: Heurística de Latência (Apenas estimativa baseada em Stack TCP)
        # Windows tende a ter um tempo de processamento de stack ligeiramente diferente
        if rtt < 10:
            return "Local Node / Low-latency Unix"
        elif 10 <= rtt < 60:
            return "Linux/Unix Host"
        else:
            return "Remote Host (Possibly Windows/Cloud Firewall)"

    @staticmethod
    def analyze_firewall(status_code):
        """
        Traduz códigos de erro de socket em políticas de firewall.
        """
        # Códigos de erro padrão do socket/OS
        mapping = {
            11: "FILTERED (Silent Drop / Stateless)",
            10060: "FILTERED (Timeout)",
            111: "CLOSED (Refused - No Firewall)",
            10061: "CLOSED (Refused by Host)",
            0: "UNFILTERED (Open/Accessible)"
        }
        return mapping.get(status_code, f"UNKNOWN STATE ({status_code})")