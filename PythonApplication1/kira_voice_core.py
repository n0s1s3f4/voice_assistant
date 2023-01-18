import pyaudio
from vosk import Model, KaldiRecognizer
import pyttsx3
import mysql.connector
import socket
import json
import difflib
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


names = ['саша','саня','сашка','сашенька','санечка','александр','железяка','консерва','бот',"саш","сша"]         # ИМЕНА АССИСТЕНТА





def say(text):
    if engine._inLoop:
         engine.endLoop()
    engine.say(text) 
    engine.runAndWait() 
    engine.stop()                    # ПРОИЗНОСИМ ФРАЗУ
def create_connection(host_name, user_name, user_password,db_name,db_port):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name,
            port = db_port
        )
        print("Connection to MySQL DB successful")
    except Error as e:
        print("The error '{e}' occurred")

    return connection
def get_talkAI_database():
    global count
    cursor.execute("SELECT question FROM kira_talk_ai ORDER BY id") 
    questions = cursor.fetchall() # get questions
    cursor.execute("SELECT answer FROM kira_talk_ai ORDER BY id") 
    answers = cursor.fetchall() # get answers
    cursor.execute("SELECT COUNT(*) FROM kira_talk_ai")
    count = cursor.fetchall()[0][0]# get rows count
    print(count)
    i=0
    AIdictPartial=[0,'','']
    while i<count:
        AIdictPartial=[0,questions[i][0],answers[i][0]]
        AIdict.insert(i,AIdictPartial)
        i=i+1
    return AIdict  # В РЕЗУЛЬТАТЕ ПОЛУЧАЕМ МНОГОМЕРНЫЙ МАССИВ, ОДИН ЭЛЕМЕНТ ЭТО [0, ВОПРОС,ОТВЕТ]
def get_talkAI_answer(phrase):
    result_dict = AIdict
    i=0
    while i<count:
        result_dict[i][0]=difflib.SequenceMatcher(a=phrase,b=result_dict[i][1]).ratio()
        i = i+1
    result_dict.sort(reverse=True) # полученный массив [ совпадение, вопрос, ответ] сортируем
    return result_dict[0][2] #возвращаем ответ с наибольшим совпадением по результату сортировки

def recognize():  
    while True:
        try:
            data = stream.read(6000, exception_on_overflow=False)
            if len(data) == 0:
                break
            if rec.AcceptWaveform(data):
                res = json.loads(rec.Result())['text']
                print('Распознал:   ' + res)
                if res == '':
                    continue
                else:
                    resSPLITTED=res.split()
                    search_name(res,resSPLITTED,names)
            else:
                partres = json.loads(rec.PartialResult())['partial']
                print('Слушаю:   ' + partres)                          # РАСПОЗНАВАНИЕ РЕЧИ И ОТПРАВКА ДАННЫХ В МЕТОД ПОИСКА ОБРАЩЕНИЯ
        except Exception as e:
            print('опять наебланил микрофон, ошибка')                  # СЛУШАЕМ И РАСПОЗНАЕМ РЕЧЬ
            print(e)
            continue                                                   # СЛУШАЕМ ЭФИР И ЛОВИМ СЛОВА

def search_name(res,resSPLITTED,names):  
    i = 0
    while i < len(resSPLITTED):
        if resSPLITTED[i] in names:
            check_command(resSPLITTED)
            break
        else:
            i = i + 1    # ИЩЕМ В РАСПОЗНАННОЙ ФРАЗЕ ОБРАЩЕНИЕ К АССИСТЕНТУ
connection = create_connection("localhost", "root", "123098","kira_db","3306")
cursor = connection.cursor()
AIdict = []
if 1==1:
    get_talkAI_database()
    recognize()