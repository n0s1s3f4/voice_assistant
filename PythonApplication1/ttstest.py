from paho.mqtt import publish


def main():  
    msgs = [{'topic': "mqtt/paho/test", 'payload': "hello"},
            {'topic': "mqtt/paho/test", 'payload': "world"}]
    publish.multiple(msgs, hostname="localhost", auth={'username':"admin", 'password':"admin"})

if __name__ == "__main__":  
    main()