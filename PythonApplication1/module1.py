import socket
from threading import Thread


def listen():
    while True:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                print('начал слушать')
                HOST = '127.0.0.1'  # The server's hostname or IP address
                PORT = 65431        # The port used by the server
                s.bind((HOST, PORT))
                s.listen()
                conn, addr = s.accept()
                with conn:
                    print('Connected by', addr)
                    while True:
                        final_command = conn.recv(1024).decode("utf-8")
                        if not final_command:
                            break
                        else:
                            print('Получил команду:   ' + final_command)

def send():


if 1==1:

    send_Thread = Thread(target=send)
    listen_Thread = Thread(target=listen)
    send_Thread.start()
    listen_Thread.start()