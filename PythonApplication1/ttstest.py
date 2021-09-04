import pyttsx3

engine = pyttsx3.init()    # Инициализировать голосовой движок.
voices = engine.getProperty('voices')

for voice in voices:    # голоса и параметры каждого
    print('------')
    print(f'Имя: {voice.name}')
    print(f'ID: {voice.id}')
    print(f'Язык(и): {voice.languages}')
    print(f'Пол: {voice.gender}')
    print(f'Возраст: {voice.age}')