import requests
from vosk import Model, KaldiRecognizer
import pyaudio
import pyttsx3
import json
import time
p = pyaudio.PyAudio()               # ИНИЦИАЛИЗАЦИЯ РАБОТЫ СО ЗВУКОМ
stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=16000) #НАСТРОИЛИ ПОТОК С МИКРОФОНА
stream.start_stream()               # НАЧАЛИ ПРИНИМАТЬ ПОТОК С МИКРОФОНА
engine = pyttsx3.init()             # ИНИЦИАЛИЗАЦИЯ ДВИЖКА РАЗГОВОРА
engine.setProperty('rate', 170)     # СКОРОСТЬ
engine.setProperty('volume', 0.9)   # ГРОМКОСТЬ
engine.setProperty('voice', 'ru')   # ЗАДАЕМ ГОЛОС ПО УМОЛЧАНИЮ (по факту ничего не делает но без нее ничего не работает)
voices = engine.getProperty('voices')
model = Model("model-ru")           # ИНИЦИАЛИЗАЦИЯ МОДЕЛИ
rec = KaldiRecognizer(model, 16000) # ИНИЦИАЛИЗАЦИЯ РАСПОЗНАВАНИЯ РЕЧИ
for voice in voices:
    if voice.name == 'Aleksandr':
        engine.setProperty('voice', voice.id)
def recognize():  
    while True:
        try:
            data = stream.read(2000)
            if len(data) == 0:
                break
            if rec.AcceptWaveform(data):
                res = json.loads(rec.Result())['text']
                print('Распознал   ' + res)

                engine.say('я фыафв')
                engine.runAndWait
                time.sleep(2)
            else:
                partres = json.loads(rec.PartialResult())['partial']
                print('Слушаю   ' + partres)                  # РАСПОЗНАВАНИЕ РЕЧИ И ОТПРАВКА ДАННЫХ В МЕТОД ПОИСКА ОБРАЩЕНИЯ
        except Exception as e:
            print('опять наебланил микрофон, ошибка')
recognize()