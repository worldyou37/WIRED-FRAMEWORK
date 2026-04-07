import socket
import time

class ConnectionHandler:
    """
    O 'Wired' - Responsável pela interface bruta com a camada de transporte.
    Suporta IPv4, IPv6 e análise de latência em tempo real.
    """

    @staticmethod
    def create_probe(target, port, timeout=1.0, ipv6=False):
        """
        Cria uma sonda TCP e retorna o estado detalhado da porta.
        Retorna: (status, rtt, socket_obj ou None)
        Status: 0 (Open), 11 (Timeout/Filtered), -1 (Error/Closed)
        """
        family = socket.AF_INET6 if ipv6 else socket.AF_INET
        sock = socket.socket(family, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        
        start_time = time.perf_counter()
        try:
            # connect_ex retorna 0 para sucesso (aberto)
            result = sock.connect_ex((target, port))
            end_time = time.perf_counter()
            
            rtt = (end_time - start_time) * 1000 # Latência em ms
            
            if result == 0:
                return 0, rtt, sock
            else:
                sock.close()
                return result, rtt, None
                
        except socket.gaierror:
            return -2, 0, None # Erro de resolução de nome
        except Exception:
            return -1, 0, None

    @staticmethod
    def grab_raw_data(sock, payload=None, buffer_size=1024):
        """
        Tenta extrair dados brutos de um socket aberto.
        Envia um payload opcional para 'acordar' o serviço.
        """
        if not sock:
            return None
            
        try:
            if payload:
                sock.send(payload)
            
            # Define um timeout curto para não travar na leitura
            sock.settimeout(2.0)
            data = sock.recv(buffer_size)
            return data.decode(errors='ignore').strip()
        except (socket.timeout, ConnectionResetError):
            return None
        except Exception:
            return None
        finally:
            sock.close()

    @staticmethod
    def get_local_ip(ipv6=False):
        """Identifica o endereço de origem na rede interna."""
        family = socket.AF_INET6 if ipv6 else socket.AF_INET
        temp_sock = socket.socket(family, socket.SOCK_DGRAM)
        try:
            # Não precisa conectar de verdade para descobrir o IP local
            target = "2001:4860:4860::8888" if ipv6 else "8.8.8.8"
            temp_sock.connect((target, 80))
            ip = temp_sock.getsockname()[0]
        except Exception:
            ip = "::1" if ipv6 else "127.0.0.1"
        finally:
            temp_sock.close()
        return ip