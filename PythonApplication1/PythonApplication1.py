from vosk import Model, KaldiRecognizer
import os
import json
import pyaudio
import pyttsx3
if not os.path.exists("model-ru"):
    print ("error model import")
    exit (1) #ПРОВЕРКА ИНИЦИАЛИЗАЦИИ РЕЧЕВОЙ МОДЕЛИ ДЛЯ РАСПОЗНАВАНИЯ

########################### ИНИЦИАЛИЗАЦИЯ МОДУЛЕЙ И КОМПОНЕНТОВ
p = pyaudio.PyAudio()               #ИНИЦИАЛИЗАЦИЯ РАБОТЫ СО ЗВУКОМ
stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000) #НАСТРОИЛИ ПОТОК С МИКРОФОНА
stream.start_stream()               #НАЧАЛИ ПРИНИМАТЬ ПОТОК С МИКРОФОНА

model = Model("model-ru")           #ИНИЦИАЛИЗАЦИЯ МОДЕЛИ
rec = KaldiRecognizer(model, 16000) #ИНИЦИАЛИЗАЦИЯ РАСПОЗНАВАНИЯ РЕЧИ

engine = pyttsx3.init()             #ИНИЦИАЛИЗАЦИЯ ДВИЖКА РАЗГОВОРА
engine.setProperty('rate', 200)     # СКОРОСТЬ
engine.setProperty('volume', 0.9)   # ГРОМКОСТЬ
engine.setProperty('voice', 'ru')   # ЗАДАЕМ ГОЛОС ПО УМОЛЧАНИЮ (по факту ничего не делает но без нее ничего не работает)
voices = engine.getProperty('voices')
for voice in voices:
    if voice.name == 'Aleksandr':
        engine.setProperty('voice', voice.id)

names = ['','','','','','','','','','','','',] #ИМЕНА НА КОТОРЫЕ РЕАГИРУЕТ АССИСТЕНТ(ДОЛЖНЫ БЫТЬ ПРОИЗНЕСЕНЫ В ЛЮБОМ МЕСТЕ В ОБРАЩЕНИИ)
modes = ['управление','разговор','тишина','защита']     #СПИСОК РЕЖИМОВ БОТА
mode = modes[0]   #ТЕКУЩИЙ РЕЖИМ РАБОТЫ
print('ТЕКУЩИЙ РЕЖИМ РАБОТЫ:  '+ mode)
###########################

def mode_analyse(result): #МЕТОД ПОИСКА СЛОВ И ОТВЕТОВ НА НИХ

    if 'режим' in result:  #ОТПРАВЛЯЕМ МЕНЯТЬ РЕЖИМ РАБОТЫ
        mod_change(result) 

    elif mode == modes[0]: #ЕСЛИ АКТИВЕН РЕЖИМ УПРАВЛЕНИЯ
        utility(result)

    elif mode == modes[1]: #ЕСЛИ АКТИВЕН РЕЖИМ РАЗГОВОРА
        talk(result)

    elif mode == modes[2]: #ЕСЛИ АКТИВЕН РЕЖИМ ТИШИНЫ
        silence(result)

    elif mode == modes[3]: #ЕСЛИ АКТИВЕН РЕЖИМ ЗАЩИТЫ
        lock(result)

def mod_change(result):
    if 'режим' and 'управления' in result:
        mode = modes[0]

    elif 'режим' and 'разговора' in result:
        mode = modes[1]

    elif 'режим' and 'тишины' in result:
        mode = modes[2]

    elif 'режим' and 'защиты' in result:
        mode = modes[3]

    print('ПЕРЕКЛЮЧИЛ РЕЖИМ РАБОТЫ НА:  ' + mode)

def utility(result):

def talk(result):

def silence(result):

def lock(result):


while True: #РАСПОЗНАВАНИЕ РЕЧИ И ОТПРАВКА ДАННЫХ В МЕТОД ПОИСКА СЛОВ И ОТВЕТА НА НИХ
    data = stream.read(2000)
    if len(data) == 0:
        break
    if rec.AcceptWaveform(data):
        res = json.loads(rec.Result())['text']
        print('Распознал   ' + res)
        result = res.split()
        mode_analyse(result)
    else:
        partres = json.loads(rec.PartialResult())['partial']
        print('Слушаю   ' + partres)