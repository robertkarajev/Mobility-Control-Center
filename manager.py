import server
import mqttBrokerInfo
import logger

logger = logger.Logger(0)
topCar = 'car'
topMsg = 'message'
topAdd = 'addTag'

brokerInfo = mqttBrokerInfo.getmqttinfo()
client = server.MqttServerClient(brokerInfo[0], brokerInfo[1], brokerInfo[2], brokerInfo[3], logger)
client.createClient()
client.startConnection()
test = server.MySQLConnector(logger)


def processMsg():
    msgInfo = client.getMsg()
    logger.debug(msgInfo, topic=topMsg)
    topic = msgInfo[0]
    msg = msgInfo[1]

    # Get Path (a car wants a path (either to parking space or the exit))
    if topic == "GP":
        logger.info('car asks for path', topic=topCar)
        carInfo = msg.split(',')
        client.sendPublish(carInfo[0], test.dummyPathfinding(carInfo), 1)

    # Last Tag (the car has arrived at the destination)
    elif topic == 'LT':
        logger.info('car ' + msg + ' has arrived succesfully', topic=topCar)
        client.sendPublish(msg, test.registerArrival(msg), 1)

    # AUthorization (to authorize cars to make sure no car has the same ID)
    elif topic == 'AU':
        logger.info(msg, 'asks for auth', topic=topCar)
        client.sendPublish(msg, test.registerCar(msg), 1)

    # Read Tag (to add to database (voor opzet))
    elif topic == 'RT':
        logger.info('tagId being added to database', topic=topAdd)
        carInfo = msg.split(',')
        client.sendPublish(carInfo[0], test.addTag(carInfo[1]), 1)

    else:
        logger.error('topic of message not recognised')
    print()


while True:
    processMsg()
