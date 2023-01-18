import socket
import requests
import wikipedia
import time
import difflib
import linecache
from paho.mqtt import client as mqtt_client
from threading import Thread
import os
import datetime
import json

broker = '192.168.1.4'
port = 12765
client_id = 'core'
username = 'esp8266'
password = '123098'


weather_dict = {
    "clear" : "ясно",
    "partly-cloudy" : "малооблачно",
    "cloudy" : "облачно с прояснениями",
    "overcast" : "пасмурно",
    "drizzle" : "морось",
    "light-rain" : "небольшой дождь",
    "rain" : "дождь",
    "moderate-rain" : "умеренно сильный дождь",
    "heavy-rain" : "сильный дождь",
    "continuous-heavy-rain" : "длительный сильный дождь",
    "showers" : "ливень",
    "wet-snow" : "дождь со снегом",
    "light-snow" : "небольшой снег",
    "snow" : "снег",
    "snow-showers" : "снегопад",
    "hail" : "град",
    "thunderstorm" : "гроза",
    "thunderstorm-with-rain" : "дождь с грозой",
    "thunderstorm-with-hail" : "гроза с градом"
    
    }
 

def command(final_command):
    if final_command == 'скажи анекдот':
         say('пошел нахуй')

    if final_command == 'погода на улице':
        yandex_weather_get()

    if final_command == 'вошел в дом':
          yandex_scenario_im_home()  

    if final_command == 'вышел из дома':
        yandex_scenario_go_away()

    if final_command == 'доброе утро':
        yandex_scenario_good_morning()

    if final_command == 'спокойной ночи':
          yandex_scenario_good_night()
            

def yandex_scenario_good_night():
    url = "https://api.iot.yandex.net/v1.0/scenarios/74fdaf53-8ad4-46ad-ad1a-78d209d7e6c5/actions"

    payload={}
    headers = {
     'Authorization': 'Bearer y0_AgAEA7qh8fYYAAicxQAAAADT92BwzHtRgLXKT0CbfOOMJM_QzU_n4vI'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    say('и тебе спокойной ночи')

def yandex_scenario_good_morning():
    url = "https://api.iot.yandex.net/v1.0/scenarios/7c7b94e4-8f52-4df2-99d5-7ae56207ead0/actions"

    payload={}
    headers = {
     'Authorization': 'Bearer y0_AgAEA7qh8fYYAAicxQAAAADT92BwzHtRgLXKT0CbfOOMJM_QzU_n4vI'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    yandex_weather_get()

def yandex_scenario_im_home():
    url = "https://api.iot.yandex.net/v1.0/scenarios/dc06c949-6cba-4e52-83ed-2eb4102fc086/actions"

    payload={}
    headers = {
     'Authorization': 'Bearer y0_AgAEA7qh8fYYAAicxQAAAADT92BwzHtRgLXKT0CbfOOMJM_QzU_n4vI'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    say('с возвращением')


def yandex_scenario_go_away():
    url = "https://api.iot.yandex.net/v1.0/scenarios/66756bf6-c039-4680-9416-bcbdd4bff218/actions"

    payload={}
    headers = {
     'Authorization': 'Bearer y0_AgAEA7qh8fYYAAicxQAAAADT92BwzHtRgLXKT0CbfOOMJM_QzU_n4vI'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    say('до встречи, буду ждать')


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
    time.sleep(1)
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
            print('отправляю' + text)
            HOST = '127.0.0.1'  # The server's hostname or IP address
            PORT = 65432        # The port used by the server
            s.connect((HOST, PORT))
            s.send(text.encode())   

def get_current_hour():
    daytime = int(datetime.datetime.now().hour)
    if 0 <= daytime & daytime < 6:
        return "ночь1"
    if 6 <= daytime & daytime < 12:
        return "утро"
    if 12 <= daytime & daytime < 18:
        return "день"
    if 18 <= daytime & daytime < 23:
        return "вечер"
    if 23 <= daytime:
        return "ночь"
    

def yandex_weather_get():

    hello_phrase = ""

    time_current_string = get_current_hour()

    
    if time_current_string == "ночь":
            hello_phrase = "доброй ночи"
    if time_current_string == "ночь1":
            hello_phrase = "доброй ночи"
    if time_current_string =="утро":
            hello_phrase = "доброе утро"
    if time_current_string == "день":
            hello_phrase = "добрый день"
    if time_current_string == "вечер":
            hello_phrase = "добрый вечер"

    try:

        response = requests.request("GET",
                                   "https://api.weather.yandex.ru/v2/forecast?lat=55.75396&lon=37.620393&extra=false", 
                                   headers={'X-Yandex-API-Key': '60a29894-5bb4-4e5b-be3c-179423bc6334'},
                                   data={})
        final = response.json()
        weather_temp_current = str(final["fact"]["feels_like"])
        weather_cond_current = weather_dict[final["fact"]["condition"]]
        weather_day_temp = str(final["forecasts"][0]["parts"]["day"]["temp_avg"])
        weather_day_cond = weather_dict[str(final["forecasts"][0]["parts"]["day"]["condition"])]
        weather_evening_temp = str(final["forecasts"][0]["parts"]["evening"]["temp_avg"])
        weather_evening_cond = weather_dict[str(final["forecasts"][0]["parts"]["evening"]["condition"])]
        weather_morning_temp = str(final["forecasts"][0]["parts"]["morning"]["temp_avg"])
        weather_morning_cond = weather_dict[str(final["forecasts"][0]["parts"]["morning"]["condition"])]
    except Exception as e:
            print("Exception (weather):", e)
            pass            
        
    if time_current_string == "ночь":
        final_string = hello_phrase + ". сейчас за окном " + weather_cond_current + ". температура ощущается как " + weather_temp_current 
    if time_current_string == "ночь1":
        final_string = hello_phrase + ". сейчас за окном " + weather_cond_current + ". температура ощущается как " + weather_temp_current+ ". утром будет " + weather_evening_cond + ". на термометре будет " + weather_morning_temp + ". днем скорее всего будет " + weather_day_cond + ". градусник покажет " + weather_day_temp + ". а вечером " + weather_evening_cond + ". температура " + weather_evening_temp
    if time_current_string == "утро":
         final_string = hello_phrase + ". сейчас за окном " + weather_cond_current + ". температура ощущается как " + weather_temp_current + ". днем скорее всего будет " + weather_day_cond + ". градусник покажет " + weather_day_temp + ". а вечером " + weather_evening_cond + ". температура " + weather_evening_temp   
    if time_current_string == "день":
         final_string = hello_phrase + ". сейчас за окном " + weather_cond_current + ". температура ощущается как " + weather_temp_current + ". вечером будет " + weather_evening_cond + ". градусник покажет " + weather_evening_temp       
    if time_current_string == "вечер":
         final_string = hello_phrase + ". сейчас за окном " + weather_cond_current + ". температура ощущается как " + weather_temp_current
    say(final_string)

    

global client
#client = connect_mqtt()
if 1==1:
    time.sleep(3)
#    say('ядро запущено')
    


    listen()

