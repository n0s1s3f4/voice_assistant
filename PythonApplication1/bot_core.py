import socket
import pyttsx3
import requests
import wikipedia
import time
from paho.mqtt import publish
from paho.mqtt import client






 

def command(final_command):
    print(final_command)
    if final_command == 'скажи анекдот':
         say('пошел нахуй')
    if final_command == 'погода на улице':
        weather_check()
    if final_command == 'погода дома':
         serial_dht11_check()
    if final_command == 'включение лампы':
        lamp_mqtt('lamp on')
    if final_command == 'выключение лампы':
        lamp_mqtt('lamp off')       # АНАЛИЗИРУЕМ ПОЛУЧЕННЫЕ ДАННЫЕ
def weather_check():                    
    try:
        weather_get = requests.get("http://api.openweathermap.org/data/2.5/weather",
                     params={'id': 524901, 'units': 'metric', 'lang': 'ru', 'APPID': "c5b6115662d7ea1abfcbea49d146c427"})
        weather = weather_get.json()
        #print("conditions:", weather['weather'][0]['description']) # СЛОВЕСНОЕ ОПИСАНИЕ ПОГОДЫ
        #print("temp:", weather['main']['temp'])                    # ТЕМПЕРАТУРА
        #print("temp_min:", weather['main']['temp_min'])            # МИНИМАЛЬНАЯ ТЕМПЕРАТУРА
        #print("temp_max:", weather['main']['temp_max'])            # МАКСИМАЛЬНАЯ ТЕМПЕРАТУРА
    except Exception as e:
        print("Exception (weather):", e)
        say('не могу получить данные')
        pass              # ПОЛУЧЕНИЕ ИНФОРМАЦИИ О ПОГОДЕ ЗА ОКНОМ

    say('за окном' +  str(weather['weather'][0]['description']) + 'температура воздуха' + str(int(weather['main']['temp'])) + 'градусов')              # ПАРСИМ И ПРОИЗНОСИМ ИНФОРМАЦИЮ О ПОГОДЕ НА УЛИЦЕ
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
def lamp_mqtt(data):
    msg = [{'topic': "mqtt/paho/test", 'payload': data}]
    publish.multiple(msg, hostname="192.168.1.22", port="1883", auth={'username':"admin", 'password':"admin"})

if 1==1:
    time.sleep(5)
    say('ядро запущено')
    listen()