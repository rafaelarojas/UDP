import socket

SERVER_IP = "127.0.0.1"
SERVER_PORT = 12345
BUFFER_SIZE = 1024

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((SERVER_IP, SERVER_PORT))
server_socket.listen(1)

print(f"Servidor TCP rodando em {SERVER_IP}:{SERVER_PORT}")

while True:
    conn, client_address = server_socket.accept()
    print(f"Conexão estabelecida com {client_address}")
    
    data = conn.recv(BUFFER_SIZE)
    print(f"Recebido: {data.decode()}")
    
    conn.sendall(b"Vai Corinthians")
    conn.close()
