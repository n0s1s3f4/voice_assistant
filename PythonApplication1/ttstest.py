import serial
ser = serial.Serial('com4', 9600)
val = input()
if val == '3':
    val = '3'
    hum = ''
    temp = ''
    ser.write(val.encode())
    hum_p = ser.read()
    hum_p = hum_p.decode("ascii")
    hum = hum_p
    hum_p = ser.read()
    hum_p = hum_p.decode("ascii")
    hum = hum + hum_p
    temp_p = ser.read()
    temp_p = temp_p.decode("ascii")
    temp = temp_p
    temp_p = ser.read()
    temp_p = temp_p.decode("ascii")
    temp = temp + temp_p
    print(hum)
    print(temp)