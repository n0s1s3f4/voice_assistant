from vosk import Model, KaldiRecognizer
import os
import json
import pyaudio
import pyttsx3
import difflib
from threading import Thread
import time
import socket
###########################                                           ### ИНИЦИАЛИЗАЦИЯ МОДУЛЕЙ И КОМПОНЕНТОВ ###
p = pyaudio.PyAudio()                                                                                            # ИНИЦИАЛИЗАЦИЯ РАБОТЫ СО ЗВУКОМ
model = Model("model-ru")                                                                                        # ИНИЦИАЛИЗАЦИЯ МОДЕЛИ
rec = KaldiRecognizer(model, 16000)                                                                              # ИНИЦИАЛИЗАЦИЯ РАСПОЗНАВАНИЯ РЕЧИ
stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=16000)             # НАСТРОИЛИ ПОТОК С МИКРОФОНА
stream.start_stream()                                                                                            # НАЧАЛИ ПРИНИМАТЬ ПОТОК С МИКРОФОНА
engine = pyttsx3.init()                                                                                          # ИНИЦИАЛИЗАЦИЯ ДВИЖКА РАЗГОВОРА
engine.setProperty('rate', 200)                                                                                  # СКОРОСТЬ
engine.setProperty('volume', 0.9)                                                                                # ГРОМКОСТЬ
engine.setProperty('voice', 'ru')                                                                                # ЗАДАЕМ ГОЛОС ПО УМОЛЧАНИЮ (по факту ничего не делает но без нее ничего не работает)
voices = engine.getProperty('voices')
names = ['саша','саня','сашка','сашенька','санечка','александр','железяка','консерва','бот']                     # ИМЕНА АССИСТЕНТА
mode = 0                                                                                                       # РЕЖИМЫ РАБОТЫ АССИСТЕНТА (1 - ГОВОРИМ, 0 - ПРИНИМАЕМ ТЕКСТ)
###########################

###########################                                            ### КОМАНДЫ ВЫПОЛНЯЕМЫЕ АССИСТЕНТОМ ###   
commands = [
['погода на улице',        'погода','погодой','улице','за','окном'],

['погода дома',            'комнате','температура','влажность','влажностью','температурой', 'в', 'дома','погода','доме'],

['включение лампы',        'включи','свет','посвети','мне'],

['выключение лампы',       'выключи','свет','хватит','светить'],

['скажи анекдот',          'расскажи','мне','анекдот']
 ]

###########################
def recognize_text():
    while True:
        res = input()
        result = res.split()
        search_name(result,names)            
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
            continue                  # СЛУШАЕМ ЭФИР И ЛОВИМ СЛОВА
def search_name(result,names):       
    i = 0
    while i < len(result):
        if result[i] in names:
            answer(result)
            break
        else:
            i = i + 1    # ИЩЕМ В РАСПОЗНАННОЙ ФРАЗЕ ОБРАЩЕНИЕ К АССИСТЕНТУ
def answer(result):                  
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
        print('Наибольшее совпадение -   ' + final_command)
        send(final_command)
    else:
        final_command = 'неопознанная команда'
        print('не смог распознать команду')
        say('я вас не понял')               # ГЕНЕРАЦИЯ ОТВЕТОВ ПОСЛЕ ПОЛУЧЕНИЯ КОМАНДЫ
def listen():
    while True:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                print('начал слушать')
                HOST = '127.0.0.1'  # The server's hostname or IP address
                PORT = 65432        # The port used by the server
                s.bind((HOST, PORT))
                s.listen()
                conn, addr = s.accept()
                with conn:
                    print('Connected by', addr)
                    while True:
                        text_to_say = conn.recv(1024).decode("utf-8")
                        if not text_to_say:
                            break
                        else:
                            print('Получил текст для озвучки:   ' + text_to_say)
                            say(text_to_say)                     # СЛУШАЕМ ЗАПРОСЫ ОТ ЯДРА
def send(final_command):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            print('отправляю')
            HOST = '127.0.0.1'  # The server's hostname or IP address
            PORT = 65431        # The port used by the server
            s.connect((HOST, PORT))
            s.send(final_command.encode())          # ОТПРАВЛЯЕМ ЗАПРОС В ЯДРО
def say(text):
    engine.say(text)
    engine.runAndWait() 
    engine.stop()                    # ПРОИЗНОСИМ ФРАЗУ

if 1==1:                             # ОСНОВНОЙ ЦИКЛ РАБОТЫ
    if mode == 1:
        say('ассистент запущен')
        listen_Thread = Thread(target=listen)            # ТОЧКА ВХОДА В ПРОСЛУШИВАНИЕ ЗАПРОСОВ ОТ ЯДРА
        listen_Thread.start()
        recognize()                                      # ТОЧКА ВХОДА В РАСПОЗНАВАНИЕ

    if mode == 0:
        listen_Thread = Thread(target=listen)            # ТОЧКА ВХОДА В ПРОСЛУШИВАНИЕ ЗАПРОСОВ ОТ ЯДРА
        listen_Thread.start()
        recognize_text()                                      # ТОЧКА ВХОДА В РАСПОЗНАВАНИЕ