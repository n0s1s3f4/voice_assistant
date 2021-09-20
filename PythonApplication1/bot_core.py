import socket
import serial
import pyttsx3
import requests
ser = serial.Serial('COM5', 9600)   # НАЗНАЧАЕМ ПОРТ ОБЩЕНИЯ С КОНТРОЛЛЕРОМ






 

def command(final_command):
    if final_command == 'скажи анекдот':
         say('пошел нахуй')
    if final_command == 'погода на улице':
        weather_check()
    if final_command == 'погода дома':
         serial_dht11_check()
    if final_command == 'включение лампы':
        lamp('on')
    if final_command == 'выключение лампы':
        lamp('off')       # АНАЛИЗИРУЕМ ПОЛУЧЕННЫЕ ДАННЫЕ
def serial_dht11_check():
    time.sleep(2)
    val = '3'
    ser.write(val.encode())
    hum_p = ser.read()
    hum_p = hum_p.decode("ascii")
    dht11result[0] = hum_p
    hum_p = ser.read()
    hum_p = hum_p.decode("ascii")
    dht11result[0] = dht11result[0] + hum_p
    temp_p = ser.read()
    temp_p = temp_p.decode("ascii")    #[hum, temp]
    dht11result[1] = temp_p
    temp_p = ser.read()
    temp_p = temp_p.decode("ascii")
    dht11result[1] = dht11result[1] + temp_p
    print('DHT11: Влажность ' + dht11result[0] + ' %, Температура ' + dht11result[1] + ' (c)')
    return dht11result         # ПОЛУЧЕНИЕ ИНФОРМАЦИИ С ДАТЧИКА ПОГОДЫ РАЗ В 5 СЕКУНД
def room_weather_check(result):
        if 'температура' and 'температурой' not in result:
            say('Влажность в комнате ' + dht11result[0] + ' процентов')
        if 'влажность' and 'влажностью' not in result:
            say('Температура в комнате ' + dht11result[1] + ' по цельсию')
        if ('влажность' or 'влажностью') and ('температура' or 'температурой') in result:
            say('Влажность в комнате ' + dht11result[0] + ' процентов ' + ' а Температура в комнате ' + dht11result[1] + ' по цельсию')   # ВЫВОДИМ ИНФОРМАЦИЮ О ПОГОДЕ В КОМНАТЕ
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
def lamp(switch):
        if switch == 'on':
            val = 4
        elif switch == 'off':
            val = 5
        val = str(val)
        ser.write(val.encode())                 # УПРАВЛЯЕМ ПОДКЛЮЧЕННОЙ К КОНТРОЛЛЕРУ ЛАМПОЙ ЧЕРЕЗ РЕЛЕ

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


if 1==1:
    listen()