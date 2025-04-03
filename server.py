import socket
import struct

s = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(0x0003))  # Cria um socket RAW para capturar pacotes de rede
dest_port = 1200  # Porta de destino que queremos filtrar

def checksum(data):
    if len(data) % 2:  # Adiciona um byte extra se o tamanho for ímpar
        data += b'\x00'
    total = sum((data[i] << 8) + data[i + 1] for i in range(0, len(data), 2))  # Soma os pares de bytes
    while total > 0xFFFF:  # Trata o overflow do checksum
        total = (total & 0xFFFF) + (total >> 16)
    return ~total & 0xFFFF  # Retorna o complemento de 16 bits

while True:
    raw_data, addr = s.recvfrom(65535)  # Captura pacotes de até 65535 bytes
    eth_length = 14  # Tamanho do cabeçalho Ethernet
    ip_header = raw_data[eth_length:eth_length + 20]  # Extraindo o cabeçalho IP
    iph = struct.unpack('!BBHHHBBH4s4s', ip_header)  # Desempacotando o cabeçalho IP
    protocol = iph[6]  # Protocolo do cabeçalho IP

    if protocol != 17:  # Filtra apenas pacotes UDP (protocolo 17)
        continue

    udp_start = eth_length + 20  # Índice de início do cabeçalho UDP
    udp_header = raw_data[udp_start:udp_start + 8]  # Extraindo o cabeçalho UDP
    udph = struct.unpack('!HHHH', udp_header)  # Desempacotando o cabeçalho UDP
    src_port, received_dest_port, _, received_checksum = udph  # Obtendo os valores do cabeçalho UDP

    if received_dest_port == dest_port:  # Filtra apenas pacotes para a porta especificada
        data = raw_data[udp_start + 8:]  # Obtém o payload do pacote
        source_ip = iph[8]  # Endereço IP de origem
        dest_ip = iph[9]  # Endereço IP de destino

        # Criando o pseudo-cabeçalho para verificação do checksum
        pseudo_header = struct.pack('!4s4sBBH',
            source_ip, dest_ip, 0, socket.IPPROTO_UDP, 8 + len(data)
        )
        udp_header_zero = struct.pack('!HHHH', src_port, dest_port, 8 + len(data), 0)
        calculated_checksum = checksum(pseudo_header + udp_header_zero + data)

        if calculated_checksum == received_checksum:  # Verifica a integridade do checksum
            print(f"{socket.inet_ntoa(source_ip)}{received_checksum:#04x}")

        print(f"{dest_port}: {data.decode(errors='ignore')}")
