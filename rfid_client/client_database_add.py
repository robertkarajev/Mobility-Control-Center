from client import MQTTClient as mc
import json
<<<<<<< HEAD
import main
import configpaser as cp

read_file = cp.ConfigParser()
read_file.read('read_file.ini')
ip = read_file['serverinformation']['IP']
=======
import time
>>>>>>> development


class MQTTClient(mc):
    def on_message(self, client, userdata, message):
        if message.topic == self.name:
            msg = json.loads(str(message.payload.decode('utf-8')))
            if not self.authorized:
                self.authLogic(msg)
            else:
                self.msg = msg
        else:
            print('message that was not intended for you has been received')

    def sendTag(self, tagId, msg):
        self.msg = msg
        self.sendPublish('RT', self.name + ',' + str(tagId), 1)  # ReadTag
        start = time.time()
        counter = 0
        while self.msg == 'get':
            if time.time() - start > self.retrySendingAfterSeconds:
                if counter >= self.maxAmountRetriesSending:
                    return 'took too long try sending new tag'
                print('retry sending ReadTag')
                self.sendPublish('RT', self.name + ',' + str(tagId), 1)  # ReadTag
                counter += 1
                start = time.time()
        return self.msg
<<<<<<< HEAD

    def __init__(self, broker_address, localTesting, password='', broker_port=1883):
        self.name = self.randomString(idLength)
        self.authorized = False
        Connected = False  # global variable for the state of the connection

        self.broker_address = broker_address   # Broker address
        if localTesting:
            self.broker_address = "127.0.0.1"  # Broker address
        self.port = broker_port                # Broker port
        self.user = self.name                  # Connection username
        self.password = self.randomString(8)   # Connection password

        self.client = mqttClient.Client(self.name)                      # create new instance
        self.client.username_pw_set(self.user, password=self.password)  # set username and password
        self.client.on_connect = self.on_connect                        # attach function to callback
        self.client.on_message = self.on_message                        # attach function to callback
        self.msg = ''

        print('broker address: ' + self.broker_address)

        try:
            self.client.connect(self.broker_address, port=self.port)  # connect to broker
        except:
            print('could not connect, continue trying')

        self.client.loop_start()  # start the loop
        self.getAuth()


# (broker_ip, localTesting, password='', broker_port='1833')
mqttclient = MQTTClient(ip, True)
while True:
    print('Enter new RFID tag: ')
    tagRead = str(input())
    print(mqttclient.sendTag(tagRead, 'get'))
=======
>>>>>>> development
