import socket
import struct

payload = b"vai corinthians"  # Dados que serão enviados

def checksum(data):
    if len(data) % 2:  # Se for ímpar, adiciona um byte extra
        data += b'\x00'
    total = sum((data[i] << 8) + data[i + 1] for i in range(0, len(data), 2))
    while total > 0xFFFF:  # Ajusta caso o total ultrapasse 16 bits
        total = (total & 0xFFFF) + (total >> 16)
    return ~total & 0xFFFF  # Retorna o complemento de 16 bits

# Definição de IPs e portas
source_ip = "127.0.0.1"
dest_ip = "127.0.0.1"
source_port = 54321
dest_port = 1200

# Criando o cabeçalho IP (IPv4, sem opções)
ip_header = struct.pack(
    '!BBHHHBBH4s4s',
    0x45,  # Versão IPv4 (4) e tamanho do cabeçalho (5 -> 20 bytes)
    0,  # Tipo de serviço (ToS)
    20 + 8 + len(payload),  # Comprimento total (IP + UDP + payload)
    12345,  # ID do pacote
    0,  # Offset do fragmento
    64,  # Tempo de vida (TTL)
    socket.IPPROTO_UDP,  # Protocolo UDP (17)
    0,  # Checksum (inicialmente 0, será recalculado)
    socket.inet_aton(source_ip),
    socket.inet_aton(dest_ip)
)

# Calcula o checksum do cabeçalho IP
ip_checksum = checksum(ip_header)
ip_header = struct.pack(
    '!BBHHHBBH4s4s',
    0x45, 0, 20 + 8 + len(payload), 12345, 0, 64,
    socket.IPPROTO_UDP, ip_checksum,
    socket.inet_aton(source_ip), socket.inet_aton(dest_ip)
)

# Criando o cabeçalho UDP
udp_header = struct.pack(
    '!HHHH',
    source_port,
    dest_port,
    8 + len(payload),  # Comprimento total do UDP
    0  # Checksum (será recalculado)
)

# Criando pseudo-cabeçalho para calcular checksum UDP
pseudo_header = struct.pack(
    '!4s4sBBH',
    socket.inet_aton(source_ip), socket.inet_aton(dest_ip), 0,
    socket.IPPROTO_UDP, 8 + len(payload)
)

# Calcula checksum UDP
udp_checksum = checksum(pseudo_header + udp_header + payload)

# Atualiza o cabeçalho UDP com o checksum correto
udp_header = struct.pack(
    '!HHHH', source_port, dest_port, 8 + len(payload), udp_checksum
)

# Monta o pacote final (IP + UDP + payload)
packet = ip_header + udp_header + payload

# Envio do pacote usando RAW socket
s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
s.sendto(packet, (dest_ip, 0))
print("Checksum checked") 