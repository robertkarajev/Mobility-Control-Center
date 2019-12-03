import server
import mqttBrokerInfo

brokerInfo = mqttBrokerInfo.getmqttinfo()
client = server.MQTTServer(brokerInfo[0], brokerInfo[1], brokerInfo[2], brokerInfo[3], False)
test = server.mySQLconnector()


def processMsg():
    msgInfo = client.getMsg()
    print(msgInfo)
    topic = msgInfo[0]
    msg = msgInfo[1]

    # Get Path (a car wants a path (either to parking space or the exit))
    if topic == "GP":
        carInfo = msg.split(',')
        client.sendPublish(carInfo[0], test.dummyPathfinding(carInfo), 1)

    # Park Arrived (the car has arrived at the destination)
    elif topic == 'LT':
        print('car ' + msg + ' has arrived succesfully')
        client.sendPublish(msg, test.carArrivedLogic(msg), 1)

    # AUthorization (to authorize cars to make sure no car has the same ID)
    elif topic == 'AU':
        client.sendPublish(msg, test.registerCar(msg), 1)

    # Read Tag (to add to database (voor opzet))
    elif topic == 'RT':
        carInfo = msg.split(',')
        print(carInfo)
        client.sendPublish(carInfo[0], test.addTag(carInfo[1]), 1)

    else:
        print('[ERROR]: topic of message not recognised')


while True:
    processMsg()
