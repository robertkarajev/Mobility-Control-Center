import client
import mqttBrokerInfo
import time

# (broker_ip, localTesting, password='', broker_port='1833')
brokerInfo = mqttBrokerInfo.getmqttinfo()
mqttClient = client.MQTTClient(brokerInfo[0], brokerInfo[1], brokerInfo[2], brokerInfo[3])
mqttClient.createClient()
mqttClient.startConnection()
time.sleep(.2)  # purely so i get a message from the server b4 i start to be able to read


def waitCardRead():
    while True:
        print('Enter new RFID tag to get path: ')
        tagRead = str(input())
        print(tagRead)
        if tagRead == 'lastTag':
            mqttClient.arrivedAtLastTag()
        else:
            path = mqttClient.getPath(tagRead)
            print(path)


waitCardRead()
