import paho.mqtt.client as mqtt #import the client1
#broker_address="192.168.1.184"
broker_address="test.mosquitto.org"
print("creating new instance")
client = mqtt.Client("P1") #create new instance
print("connecting to broker")
client.connect(broker_address) #connect to broker