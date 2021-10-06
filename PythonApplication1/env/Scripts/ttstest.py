from paho.mqtt import client as mqtt_client
import serial
import time

ser = serial.Serial('com3', 9600)

broker = '192.168.1.4'
port = 12765
client_id = 'dht'
username = 'esp8266'
password = '123098'


def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)
    # Set Connecting Client ID
    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def publish(client):
    while True:
        time.sleep(5)
        client.publish('home/hum', get_hum())
        time.sleep(5)
        client.publish('home/temp', get_temp())
        
 

def get_hum():
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
                return hum_res
def get_temp():
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
                return temp_res

def run():
    client = connect_mqtt()
    client.loop_start()
    publish(client)

if __name__ == '__main__':
    run()