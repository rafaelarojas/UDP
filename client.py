import socket
import struct

def checksum(msg):
    s = 0
    for i in range(0, len(msg), 2):
        w = (msg[i] << 8) + (msg[i+1] if i+1 < len(msg) else 0)
        s = (s + w) & 0xFFFF
    return ~s & 0xFFFF

def create_packet(data):
    src_port = 12345
    dest_port = 12345
    length = 8 + len(data)
    checksum_value = 0
    
    header = struct.pack('!HHHH', src_port, dest_port, length, checksum_value)
    checksum_value = checksum(header + data.encode())
    header = struct.pack('!HHHH', src_port, dest_port, length, checksum_value)
    return header + data.encode()

def main():
    HOST = "127.0.0.1"
    MESSAGE = "vai corinthians"
    
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_UDP)
    packet = create_packet(MESSAGE)
    
    client_socket.sendto(packet, (HOST, 12345))
    print("Mensagem enviada!")
    client_socket.close()

if __name__ == "__main__":
    main()
