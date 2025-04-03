import socket
import struct

def checksum(msg):
    s = 0
    for i in range(0, len(msg), 2):
        w = (msg[i] << 8) + (msg[i+1] if i+1 < len(msg) else 0)
        s = (s + w) & 0xFFFF
    return ~s & 0xFFFF

def main():
    HOST = "127.0.0.1"
    
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_UDP)
    server_socket.bind((HOST, 12345))
    print(f"Servidor escutando em {HOST}:12345...")

    while True:
        data, addr = server_socket.recvfrom(1024)
        header = data[:8]
        message = data[8:]

        src_port, dest_port, length, recv_checksum = struct.unpack('!HHHH', header)
        calc_checksum = checksum(header[:6] + b'\x00\x00' + message)

        if recv_checksum == calc_checksum:
            print(f"Mensagem recebida de {addr}: {message.decode()} (Checksum válido)")
        else:
            print(f"Mensagem recebida de {addr} com checksum inválido!")
        break

    server_socket.close()

if __name__ == "__main__":
    main()
