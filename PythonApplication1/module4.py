# coding=utf-8

import pyttsx3

engine = pyttsx3.init()    # ���������������� ��������� ������.
voices = engine.getProperty("voices")

for voice in voices:    # ������ � ��������� �������
    print('------')
    print(f'{voice.name}')
    print(f'{voice.id}')
    print(f'{voice.languages}')
    print(f'{voice.gender}')
    print(f'{voice.age}')