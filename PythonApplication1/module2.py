import socket
from threading import Thread


def listen():


def send():




if 1==1:

    send_Thread = Thread(target=send)
    listen_Thread = Thread(target=listen)
    send_Thread.start()
    listen_Thread.start()