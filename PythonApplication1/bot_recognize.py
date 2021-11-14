from vosk import Model, KaldiRecognizer
import os
import json
import pyaudio
import pyttsx3
import difflib
from threading import Thread
import time
import socket
import linecache
###########################                                           ### ИНИЦИАЛИЗАЦИЯ МОДУЛЕЙ И КОМПОНЕНТОВ ###
model = Model("model-ru")                                                                                        # ИНИЦИАЛИЗАЦИЯ МОДЕЛИ
rec = KaldiRecognizer(model, 16000)                                                                              # ИНИЦИАЛИЗАЦИЯ РАСПОЗНАВАНИЯ РЕЧИ
p = pyaudio.PyAudio()                                                                                            # ИНИЦИАЛИЗАЦИЯ РАБОТЫ СО ЗВУКОМ
stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=48000)             # НАСТРОИЛИ ПОТОК С МИКРОФОНА
stream.start_stream()                                                                                            # НАЧАЛИ ПРИНИМАТЬ ПОТОК С МИКРОФОНА
engine = pyttsx3.init()                                                                                          # ИНИЦИАЛИЗАЦИЯ ДВИЖКА РАЗГОВОРА
engine.setProperty('rate', 200)                                                                                  # СКОРОСТЬ
engine.setProperty('volume', 0.9)                                                                                # ГРОМКОСТЬ
engine.setProperty('voice', 'ru')                                                                                # ЗАДАЕМ ГОЛОС ПО УМОЛЧАНИЮ (по факту ничего не делает но без нее ничего не работает)
voices = engine.getProperty('voices')
names = ['саша','саня','сашка','сашенька','санечка','александр','железяка','консерва','бот',"саш","сша"]         # ИМЕНА АССИСТЕНТА
mode = 1                                                                                                         # РЕЖИМЫ РАБОТЫ АССИСТЕНТА (1 - ГОВОРИМ, 0 - ПРИНИМАЕМ ТЕКСТ)
string_count = 8000                                                                                              #количество строк в базе данных
###########################

###########################                                            ### КОМАНДЫ ВЫПОЛНЯЕМЫЕ АССИСТЕНТОМ ###   
commands = [
['погода на улице',        'погода','погодой','улице','за','окном'],

['включение лампы',        'включи','свет','посвети','мне'],

['выключение лампы',       'выключи','свет','хватит','светить'],

['скажи анекдот',          'расскажи','мне','анекдот'],

['таймер',                 'поставь','таймер','на','часов','минут'],

["сон",                     "спать","пора","сон","погаси","всё"]

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
            data = stream.read(6000, exception_on_overflow=False)
            if len(data) == 0:
                break
            if rec.AcceptWaveform(data):
                res = json.loads(rec.Result())['text']
                print('Распознал:   ' + res)
                result = res.split()
                search_name(result,names)
            else:
                partres = json.loads(rec.PartialResult())['partial']
                print('Слушаю:   ' + partres)                          # РАСПОЗНАВАНИЕ РЕЧИ И ОТПРАВКА ДАННЫХ В МЕТОД ПОИСКА ОБРАЩЕНИЯ
        except Exception as e:
            print('опять наебланил микрофон, ошибка')                  # СЛУШАЕМ И РАСПОЗНАЕМ РЕЧЬ
            print(e)
            continue                                                   # СЛУШАЕМ ЭФИР И ЛОВИМ СЛОВА


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
        print('Наибольшее совпадение -     ' + final_command)
        send(final_command)
    else:
        if mode == 1:
            print(result)
            say(talk(result))
        else:
            print(talk(result))
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
                            if mode == 1:
                                print('Получил текст для озвучки:   ' + text_to_say)
                                say(text_to_say)
                            else:
                                print(text_to_say)
       # СЛУШАЕМ ЗАПРОСЫ ОТ ЯДРА
def send(final_command):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            print('отправляю')
            HOST = '127.0.0.1'  # The server's hostname or IP address
            PORT = 65431        # The port used by the server
            s.connect((HOST, PORT))
            s.send(final_command.encode())          # ОТПРАВЛЯЕМ ЗАПРОС В ЯДРO

def talk(input_array):
    count = 0
    result = ''
    while count<len(input_array):
        result = result + ' ' + input_array[count]
        count = count + 1
    database = open("answer_database.txt", "r",encoding='utf-8')
    i=0
    seq_dict = {}
    sequence = ['','','']
    answer_dict = {}
    def similar(seq1,seq2):
        return difflib.SequenceMatcher(a=seq1,b=seq2).ratio()
    while i<string_count:
        line = database.readline()
        if not line:
            break
        splitted = line.split('=')
        splitted[1] = splitted[1].replace("\n","")
        sequence[0] = splitted[0]
        sequence[1] = splitted[1]
        sequence[2] = i+1
        seq_dict[sequence[2]] = similar(result,sequence[0])
        answer_dict[sequence[2]] = splitted[1]
        i=i+1
    sorted_dict = sorted(seq_dict.items(), key=lambda x: x[1])
    pre_answer = sorted_dict[string_count - 1][0]
    answer = answer_dict.get(pre_answer)
    database.close()
    return str(answer)


def say(text):
    if engine._inLoop:
         engine.endLoop()
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
        recognize_text()                          # ТОЧКА ВХОДА В РАСПОЗНАВАНИЕ