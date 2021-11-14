from paho.mqtt import client as mqtt_client
import serial
import time
from threading import Thread

broker = '192.168.1.4'
port = 12765
username='esp8266'
client_id = 'dht'
password = '123098'

temperature = ''
humidity = ''
light_switch = ""

def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

def connect_mqtt():
    # Set Connecting Client ID
    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(broker, port)
    return client



        
 

def serial_get_set():
                ser = serial.Serial('com5', 9600)   ##############
                print("serial da")
                while True:
                    time.sleep(2)
                    val = '3'
                    hum = [0,0]
                    ser.write(val.encode())
                    hum_p = ser.read()
                    hum_p = hum_p.decode("UTF-8")
                    hum[0] = hum_p                   
                    hum_p = ser.read()
                    hum_p = hum_p.decode("UTF-8")
                    hum[1] = hum_p
                    hum_res = str(hum[0] + hum[1])
                    humidity = hum_res  ####
                    val = '4'
                    temp = [0,0]
                    ser.write(val.encode())
                    temp_p = ser.read()
                    temp_p = temp_p.decode("UTF-8")
                    temp[0] = temp_p                   
                    temp_p = ser.read()
                    temp_p = temp_p.decode("UTF-8")
                    temp[1] = temp_p
                    temp_res = str(temp[0] + temp[1])
                    temperature = temp_res ###
                    time.sleep(1)
                    if light_switch == "light on":
                        val = '6'
                        ser.write(val.encode())
                    else:
                        val = '5'
                        ser.write(val.encode())

def dht_publish_data():
    lient = mqtt_client.Client("dht_publish")
    client.username_pw_set(username, password)
    client.connect(broker, port)
    while True:
        print("publish da")
        time.sleep(1)
        client.publish('home/hum', humidity)
        client.publish('home/temp', temperature)

def get_light_data():

    client = mqtt_client.Client("dht_get")
    client.username_pw_set(username, password)
    client.on_message = on_message
    client.connect(broker, port)
    client.subscribe("lcd/backlight")
    client.loop_start()
     


if 1==1:
 get_set_thread = Thread(target=serial_get_set())
 publish_thread = Thread(target=dht_publish_data())
 light_thread = Thread(target=get_light_data())
 get_set_thread.start()
 publish_thread.start()
 light_thread.start()