from vosk import Model, KaldiRecognizer
import os
import json
import pyaudio
import pyttsx3
import difflib

if not os.path.exists("model-ru"):
    print ("error model import")
    exit (1) #ПРОВЕРКА ИНИЦИАЛИЗАЦИИ РЕЧЕВОЙ МОДЕЛИ ДЛЯ РАСПОЗНАВАНИЯ

###########################                                           ### ИНИЦИАЛИЗАЦИЯ МОДУЛЕЙ И КОМПОНЕНТОВ ###
p = pyaudio.PyAudio()               # ИНИЦИАЛИЗАЦИЯ РАБОТЫ СО ЗВУКОМ
stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000) #НАСТРОИЛИ ПОТОК С МИКРОФОНА
stream.start_stream()               # НАЧАЛИ ПРИНИМАТЬ ПОТОК С МИКРОФОНА

model = Model("model-ru")           # ИНИЦИАЛИЗАЦИЯ МОДЕЛИ
rec = KaldiRecognizer(model, 16000) # ИНИЦИАЛИЗАЦИЯ РАСПОЗНАВАНИЯ РЕЧИ

engine = pyttsx3.init()             # ИНИЦИАЛИЗАЦИЯ ДВИЖКА РАЗГОВОРА
engine.setProperty('rate', 170)     # СКОРОСТЬ
engine.setProperty('volume', 0.9)   # ГРОМКОСТЬ
engine.setProperty('voice', 'ru')   # ЗАДАЕМ ГОЛОС ПО УМОЛЧАНИЮ (по факту ничего не делает но без нее ничего не работает)
voices = engine.getProperty('voices')
for voice in voices:
    if voice.name == 'Aleksandr':
        engine.setProperty('voice', voice.id)

names = ['саша','саня','сашка','сашенька','санечка','александр','железяка','консерва','бот'] #ИМЕНА НА КОТОРЫЕ РЕАГИРУЕТ АССИСТЕНТ(ДОЛЖНЫ БЫТЬ ПРОИЗНЕСЕНЫ В ЛЮБОМ МЕСТЕ В ОБРАЩЕНИИ)
modes = ['управление','разговор']    # СПИСОК РЕЖИМОВ БОТА
mode = modes[0]                     # ТЕКУЩИЙ РЕЖИМ РАБОТЫ
print('ТЕКУЩИЙ РЕЖИМ РАБОТЫ:  '+ mode)
###########################

def search_name(result,names):   #ИЩЕМ В РАСПОЗНАННОЙ ФРАЗЕ ОБРАЩЕНИЕ К АССИСТЕНТУ
    i = 0
    while i < len(result):
        if result[i] in names:
            answer(result)
            break
        else:
            i = i + 1
    


def answer(result):
   engine.say('отвечаю')
   engine.runAndWait()


while True: #РАСПОЗНАВАНИЕ РЕЧИ И ОТПРАВКА ДАННЫХ В МЕТОД ПОИСКА СЛОВ И ОТВЕТА НА НИХ
    data = stream.read(2000)
    if len(data) == 0:
        break
    if rec.AcceptWaveform(data):
        res = json.loads(rec.Result())['text']
        print('Распознал   ' + res)
        result = res.split()
        search_name(result,names)
    else:
        partres = json.loads(rec.PartialResult())['partial']
        print('Слушаю   ' + partres)