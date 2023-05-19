import socket
import requests
import wikipedia
import time
from threading import Thread
import os
import datetime
import json
from hassapi import Hass

hass = Hass(hassurl="http://192.168.1.19:8123/", token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJhMTA1NTM4MzU3MGM0YmIwOTY4ZDMxNTEwZDZjYjg0MyIsImlhdCI6MTY4NDI2MTkxMiwiZXhwIjoxOTk5NjIxOTEyfQ.x3GADWuTxpG-cdOrzYo78I-eS-nw1K5lGLACavT8ntw")


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

    if final_command == 'закрыть дверь':
          close_door_and_turn_on_lock()

    if final_command == 'открыть дверь':
          open_door()
    if final_command == 'зигби заряд':
          charge_info()


def charge_info():
    
    
    

    answer = "заряд внешней кнопки двери. " + str(hass.get_state("sensor.0x00124b00253bb307_battery").state) + " заряд внутренней кнопки. " + str(hass.get_state("sensor.0x00124b0028929001_battery").state) + " заряд датчика температуры. " + str(hass.get_state("sensor.0xa4c138e8bd67abcf_battery").state)
    say(answer)


def open_door():
    hass.turn_off("switch.sonoff_10013dd762")
    say('дверь открыта')

def close_door_and_turn_on_lock():
    hass.turn_on("input_boolean.door_button_disable")
    hass.turn_on("switch.sonoff_10013dd762")
    say('дверь заблокирована')
def yandex_scenario_good_night():
    hass.turn_off("light.lampochka")
    hass.turn_off("switch.sonoff_100117a970")
    say('и тебе спокойной ночи')

def yandex_scenario_good_morning():
    hass.turn_on("light.lampochka")
    yandex_weather_get()

def yandex_scenario_im_home():
    hass.turn_on("light.lampochka")
    say('с возвращением')


def yandex_scenario_go_away():
    hass.turn_off("light.lampochka")
    hass.turn_off("switch.sonoff_100117a970")
    hass.turn_on("input_boolean.door_button_disable")
    hass.turn_on("switch.sonoff_10013dd762")
    say('до встречи, буду ждать')





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
            HOST = '192.168.1.4'  # The server's hostname or IP address
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
            HOST = '192.168.1.7'  # The server's hostname or IP address
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

    #hello_phrase = ""

    #time_current_string = get_current_hour()

    
    #if time_current_string == "ночь":
    #        hello_phrase = "доброй ночи"
    #if time_current_string == "ночь1":
    #        hello_phrase = "доброй ночи"
    #if time_current_string =="утро":
    #        hello_phrase = "доброе утро"
    #if time_current_string == "день":
    #        hello_phrase = "добрый день"
    #if time_current_string == "вечер":
    #        hello_phrase = "добрый вечер"

    #try:

    #    response = requests.request("GET",
    #                               "https://api.weather.yandex.ru/v2/informers?lat=55.75396&lon=37.620393&extra=false", 
    #                               headers={'X-Yandex-API-Key': '60a29894-5bb4-4e5b-be3c-179423bc6334'},
    #                               data={})
    #    final = response.json()
    #    print(final)
    #    weather_temp_current = str(final["fact"]["feels_like"])
    #    weather_cond_current = weather_dict[final["fact"]["condition"]]
    #    weather_day_temp = str(final["forecast"]["parts"]["day"]["temp_avg"])
    #    weather_day_cond = weather_dict[str(final["forecast"]["parts"]["day"]["condition"])]
    #    weather_evening_temp = str(final["forecast"]["parts"]["evening"]["temp_avg"])
    #    weather_evening_cond = weather_dict[str(final["forecast"]["parts"]["evening"]["condition"])]
    #    weather_morning_temp = str(final["forecast"]["parts"]["morning"]["temp_avg"])
    #    weather_morning_cond = weather_dict[str(final["forecast"]["parts"]["morning"]["condition"])]
    #except Exception as e:
    #        print("Exception (weather):", e)
    #        pass            
        
    #if time_current_string == "ночь":
    #    final_string = hello_phrase + ". сейчас за окном " + weather_cond_current + ". температура ощущается как " + weather_temp_current 
    #if time_current_string == "ночь1":
    #    final_string = hello_phrase + ". сейчас за окном " + weather_cond_current + ". температура ощущается как " + weather_temp_current+ ". утром будет " + weather_morning_cond + ". на термометре будет " + weather_morning_temp + ". днем скорее всего будет " + weather_day_cond + ". градусник покажет " + weather_day_temp
    #if time_current_string == "утро":
    #     final_string = hello_phrase + ". сейчас за окном " + weather_cond_current + ". температура ощущается как " + weather_temp_current + ". днем скорее всего будет " + weather_day_cond + ". градусник покажет " + weather_day_temp + ". а вечером " + weather_evening_cond + ". температура " + weather_evening_temp   
    #if time_current_string == "день":
    #     final_string = hello_phrase + ". сейчас за окном " + weather_cond_current + ". температура ощущается как " + weather_temp_current + ". вечером будет " + weather_evening_cond + ". градусник покажет " + weather_evening_temp       
    #if time_current_string == "вечер":
    #     final_string = hello_phrase + ". сейчас за окном " + weather_cond_current + ". температура ощущается как " + weather_temp_current
    #say(final_string)
    say('проблемы на сервере яндекс. не могу получить данные о погоде')

    

if 1==1:
    time.sleep(3)
#    say('ядро запущено')
    


    listen()

