import pyaudio
from vosk import Model, KaldiRecognizer
import pyttsx3
import mysql.connector
import socket

model = Model("model-ru") 
rec = KaldiRecognizer(model, 16000)  

p = pyaudio.PyAudio()                                                                                            # ИНИЦИАЛИЗАЦИЯ РАБОТЫ СО ЗВУКОМ
stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=48000)             # НАСТРОИЛИ ПОТОК С МИКРОФОНА
stream.start_stream()  


engine = pyttsx3.init()                                                                                          # ИНИЦИАЛИЗАЦИЯ ДВИЖКА РАЗГОВОРА
engine.setProperty('rate', 190)                                                                                  # СКОРОСТЬ
engine.setProperty('volume', 0.9)                                                                                # ГРОМКОСТЬ
engine.setProperty('voice', 'ru')  
voices = engine.getProperty('voices')
engine.setProperty('voice', 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\MSTTS_V110_ruRU_PavelM')
engine.say("привет")



def say(text):
    if engine._inLoop:
         engine.endLoop()
    engine.say(text) 
    engine.runAndWait() 
    engine.stop()                    # ПРОИЗНОСИМ ФРАЗУ

def talk(phrase):
    similar()
