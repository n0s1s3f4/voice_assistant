import socket

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65432        # The port used by the server
final_command = 'калоед проклятый'
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
     s.connect((HOST, PORT))
     s.send(final_command.encode())
