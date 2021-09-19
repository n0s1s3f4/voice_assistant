from vosk import Model, KaldiRecognizer
import os
import json
import pyaudio
import pyttsx3
import difflib
import serial
from threading import Thread
import time
import requests
if not os.path.exists("model-ru"):
    print ("error model import")
    exit (1)                        #ПРОВЕРКА НАЛИЧИЯ РЕЧЕВОЙ МОДЕЛИ ДЛЯ РАСПОЗНАВАНИЯ



###########################                                           ### ИНИЦИАЛИЗАЦИЯ МОДУЛЕЙ И КОМПОНЕНТОВ ###
p = pyaudio.PyAudio()               # ИНИЦИАЛИЗАЦИЯ РАБОТЫ СО ЗВУКОМ
model = Model("model-ru")           # ИНИЦИАЛИЗАЦИЯ МОДЕЛИ
rec = KaldiRecognizer(model, 16000) # ИНИЦИАЛИЗАЦИЯ РАСПОЗНАВАНИЯ РЕЧИ
stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=16000) #НАСТРОИЛИ ПОТОК С МИКРОФОНА
stream.start_stream()               # НАЧАЛИ ПРИНИМАТЬ ПОТОК С МИКРОФОНА
#ser = serial.Serial('COM4', 9600)   # НАЗНАЧАЕМ ПОРТ ОБЩЕНИЯ С КОНТРОЛЛЕРОМ
engine = pyttsx3.init()             # ИНИЦИАЛИЗАЦИЯ ДВИЖКА РАЗГОВОРА
engine.setProperty('rate', 200)     # СКОРОСТЬ
engine.setProperty('volume', 0.9)   # ГРОМКОСТЬ
engine.setProperty('voice', 'ru')   # ЗАДАЕМ ГОЛОС ПО УМОЛЧАНИЮ (по факту ничего не делает но без нее ничего не работает)
voices = engine.getProperty('voices')
for voice in voices:
    if voice.name == 'Aleksandr':
        engine.setProperty('voice', voice.id)
names = ['саша','саня','сашка','сашенька','санечка','александр','железяка','консерва','бот'] #ИМЕНА НА КОТОРЫЕ РЕАГИРУЕТ АССИСТЕНТ(ДОЛЖНЫ БЫТЬ ПРОИЗНЕСЕНЫ В ЛЮБОМ МЕСТЕ В ОБРАЩЕНИИ)
dht11result = ['','']               # ПЕРЕМЕНЕЫЙ МАССИВ ДЛЯ ИСПОЛЬЗОВАНИЯ ДАННЫХ С ДАТЧИКА DHT11
###########################

###########################                                         ### КОМАНДЫ ВЫПОЛНЯЕМЫЕ САШКОЙ ###   ПЕРВЫЙ ЭЛЕМЕНТ - НАЗВАНИЕ КОМАНДЫ, ВСЕ ЧТО ПОСЛЕ САМ ТЕКСТ КОМАНДЫ
commands = [
['погода на улице','погода','погодой','улице','за','окном'],

['погода дома','комнате','температура','влажность','влажностью','температурой', 'в', 'дома','погода','доме'],

['включение лампы','включи','свет','посвети','мне'],

['выключение лампы','выключи','свет','хватит','светить'],

['скажи анекдот','расскажи','мне','анекдот']
 ]








###########################



def say(text):
    engine.say(text)
    engine.runAndWait() 
    engine.stop()                    # ГОВОРИМ
def search_name(result,names):       
    i = 0
    while i < len(result):
        if result[i] in names:
            answer(result)
            break
        else:
            i = i + 1    # ИЩЕМ В РАСПОЗНАННОЙ ФРАЗЕ ОБРАЩЕНИЕ К АССИСТЕНТУ
def recognize():  
    while True:
        try:
            data = stream.read(2000, exception_on_overflow=False)
            if len(data) == 0:
                break
            if rec.AcceptWaveform(data):
                res = json.loads(rec.Result())['text']
                print('Распознал:   ' + res)
                result = res.split()
                search_name(result,names)
            else:
                partres = json.loads(rec.PartialResult())['partial']
                print('Слушаю:   ' + partres)                  # РАСПОЗНАВАНИЕ РЕЧИ И ОТПРАВКА ДАННЫХ В МЕТОД ПОИСКА ОБРАЩЕНИЯ
        except Exception as e:
            print('опять наебланил микрофон, ошибка')                  # СЛУШАЕМ И РАСПОЗНАЕМ РЕЧЬ
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
        val = str(switch)
        ser.write(val.encode())                 # УПРАВЛЯЕМ ПОДКЛЮЧЕННОЙ К КОНТРОЛЛЕРУ ЛАМПОЙ ЧЕРЕЗ РЕЛЕ

def answer(result):                  # ГЕНЕРАЦИЯ ОТВЕТОВ ПОСЛЕ ПОЛУЧЕНИЯ КОМАНДЫ                                            КРИВО ПРОВЕРЯЕТ УСЛОВИЕ!!!
    command_dict = {}
    i = 0
    command_check_coin = 0
    while i<len(commands):                                                          # СОСТАВЛЯЕМ СЛОВАРЬ СОВПАДЕНИЯ ГОЛОСОВГО ВВОДА С ЗАПИСАННЫМИ КОМАНДАМИ
        command_dict[commands[i][0]] = len(list(set(result) & set(commands[i])))    
        i = i + 1
    sorted_command_dict = {}
    sorted_command_keys = sorted(command_dict, key=command_dict.get, reverse=True) 
    for w in sorted_command_keys:                                                   
        sorted_command_dict[w] = command_dict[w]
    for k in sorted_command_dict.values():                                          # ПРОВЕРЯЕМ СОВПАДЕНИЕ ХОТЯ БЫ С ОДНОЙ КОМАНДОЙ ( >1 СЛОВА)
        if int(list(sorted_command_dict.values())[k]) > 1:
            command_check_coin = command_check_coin + 1

    if command_check_coin>0:
        final_command = str(list(sorted_command_dict.keys())[0])
        print('Наибольшее совпадение ' + final_command)
        say('секунду')
        time.sleep(1)
    else:
        final_command = 'неопознанная команда'
        print('не смог распознать команду')
        say('я вас не понял')

    if final_command == 'скажи анекдот':
        say('пошел нахуй')
    if final_command == 'погода на улице':
        weather_check()
    if final_command == 'погода на дома':
        return
    if final_command == 'включение лампы':
        return
    if final_command == 'выключение лампы':
        return
recognize()