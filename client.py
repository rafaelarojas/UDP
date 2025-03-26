import socket

SERVER_IP = "127.0.0.1"
SERVER_PORT = 12345

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

num1 = input("Digite o primeiro número: ")
num2 = input("Digite o segundo número: ")

message = f"{num1} {num2}"
client_socket.sendto(message.encode(), (SERVER_IP, SERVER_PORT))

data, _ = client_socket.recvfrom(1024)
print(f"Resultado da soma: {data.decode()}")

client_socket.close()
