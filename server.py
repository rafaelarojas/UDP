import socket

SERVER_IP = "127.0.0.1"
SERVER_PORT = 12345
BUFFER_SIZE = 1024

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((SERVER_IP, SERVER_PORT))

print(f"Servidor UDP rodando em {SERVER_IP}:{SERVER_PORT}")

while True:
    data, client_address = server_socket.recvfrom(BUFFER_SIZE)
    print(f"Recebido de {client_address}: {data.decode()}")
    
    try:
        num1, num2 = map(int, data.decode().split())
        resultado = num1 + num2
        server_socket.sendto(str(resultado).encode(), client_address)
    except ValueError:
        server_socket.sendto(b"Erro: entrada invalida", client_address)
