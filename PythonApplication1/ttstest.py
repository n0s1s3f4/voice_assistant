import pyttsx3

tts = pyttsx3.init()

voices = tts.getProperty('voices')

# Задать голос по умолчанию
tts.setProperty('voice', 'ru') 

# Попробовать установить предпочтительный голос
for voice in voices:
    if voice.name == 'Aleksandr':
        tts.setProperty('voice', voice.id)

tts.say('Командный голос вырабатываю, товарищ генерал-полковник!')
tts.runAndWait()
