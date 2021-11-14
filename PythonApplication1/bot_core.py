9import socket
import requests
import wikipedia
import time
import difflib
import linecache
from paho.mqtt import client as mqtt_client
from threading import Thread

broker = '192.168.1.4'
port = 12765
client_id = 'core'
username = 'esp8266'
password = '123098'

 

def command(final_command):
    if final_command == 'скажи анекдот':
         say('пошел нахуй')
    if final_command == 'погода на улице':
        weather_check()
    if final_command == 'включение лампы':
        lamp('on')
    if final_command == 'выключение лампы':
        lamp('off')       # АНАЛИЗИРУЕМ ПОЛУЧЕННЫЕ ДАННЫЕ

def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)
def lamp(switch):
    if switch == 'on':
        client.publish('esp/lamp','lamp on') 
    else:
        client.publish('esp/lamp','lamp off')
def connect_mqtt():
    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def subscribe(client,topic):
    client.subscribe(topic,qos=0)



def weather_check():                    
    try:
        weather_get = requests.get("http://api.openweathermap.org/data/2.5/weather",
        params={'id': 524901, 'units': 'metric', 'lang': 'ru', 'APPID': "c5b6115662d7ea1abfcbea49d146c427"})
        weather = weather_get.json()
    except Exception as e:
        print("Exception (weather):", e)
        say('не могу получить данные')
        pass              # ПОЛУЧЕНИЕ ИНФОРМАЦИИ О ПОГОДЕ ЗА ОКНОМ

    say('за окном ' +  str(weather['weather'][0]['description']) + ' температура воздуха ' + str(int(weather['main']['temp'])) + ' градусов')              # ПАРСИМ И ПРОИЗНОСИМ ИНФОРМАЦИЮ О ПОГОДЕ НА УЛИЦЕ
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
                        command(final_command)
def say(text):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            print('отправляю')
            HOST = '127.0.0.1'  # The server's hostname or IP address
            PORT = 65432        # The port used by the server
            s.connect((HOST, PORT))
            s.send(text.encode())   

global client
client = connect_mqtt()
if 1==1:
    time.sleep(5)
    say('ядро запущено')
    


    listen()

