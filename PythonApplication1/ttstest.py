import commands
import serial
ser = serial.Serial('COM5', 9600)   # НАЗНАЧАЕМ ПОРТ ОБЩЕНИЯ С КОНТРОЛЛЕРОМ
commands.lamp('off')