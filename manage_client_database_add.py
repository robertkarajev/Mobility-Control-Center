import client_database_add as cda
import mqttBrokerInfo



brokerInfo = mqttBrokerInfo.getmqttinfo()
mqttClient = cda.MQTTClient(brokerInfo[0], brokerInfo[1], brokerInfo[2], brokerInfo[3], False)
def waitCardRead():
    while True:
        print('Enter new RFID tag: ')
        tagRead = str(input())
        print(mqttClient.sendTag(tagRead, 'get'))


waitCardRead()
