import paho.mqtt.subscribe as subscribe

topics = ['/mqtt/paho/test']

m = subscribe.simple(topics, hostname="192.168.1.22", retained=False, msg_count=2, auth={'username':"admin", 'password':"admin"})

for a in m:
    print(str(a.topic))
    print(str(a.payload))