import socket

SERVER_IP = "127.0.0.1"
SERVER_PORT = 12345

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_IP, SERVER_PORT))

client_socket.sendall(b"Vai Corinthians")

data = client_socket.recv(1024)
print(f"Resposta do servidor: {data.decode()}")

client_socket.close()
