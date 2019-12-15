import client

# (broker_ip, localTesting, password='', broker_port='1833')
brokerInfo = client.mqttBrokerInfo.getmqttinfo()
mqttClient = client.MQTTClient(brokerInfo[0], brokerInfo[1], brokerInfo[2], brokerInfo[3], False)


def waitCardRead():
    while True:
        print('Enter new RFID tag to get path: ')
        tagRead = str(input())
        path = mqttClient.getPath(tagRead)
        print(path)


waitCardRead()
