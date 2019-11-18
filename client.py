import paho.mqtt.client as mqttClient
import random
import string
import json

class MQTTClient:
	
	def __init__(self, broker_address = "127.0.0.1", broker_port = 1883, password='',):
		self.name = self.randomString(4)
		self.authorized = False
		self.broker_address = broker_address   # Broker address
		self.port = broker_port                # Broker port
		self.password = self.randomString(8)   # Connection password
		
		self.client = mqttClient.Client(self.name)                      # create new instance
		self.client.username_pw_set(self.name, self.password)  			# set username and password
		self.client.on_connect = self.on_connect                        # attach function to callback
		self.client.on_message = self.on_message                        # attach function to callback
		self.msg = ''
		self.start_connection()
	
	def start_connection(self):
		try:
			self.client.connect(self.broker_address, port=self.port)  	# connect to broker
			print(f'Broker address: {self.broker_address} port: {self.port}')
			print('Connection status is: ', self.client.is_connected())
			print(f'Connected to: {self.client._bind_address} : {self.client._bind_port}')
			self.client.loop_start() 									# start the loop
		except:
			print('could not connect, continue trying')
		self.getAuth()
	
	# create a random string containing letters and numbers with a variable length
	def randomString(self, stringLength):
		letters = string.ascii_letters + '0123456789'
		return ''.join(random.choice(letters) for i in range(stringLength))

	# callback function for when the script get a CONNACK from the broker
	# subscribes to own name so it can receive personal messages from the server-client
	def on_connect(self, client, userdata, flags, rc):
		client.subscribe(self.name, 1)
		if rc == 0:
			print("Connected to broker")
		else:
			print("Connection failed")

	# callback function for when a message is received from the broker
	def on_message(self, client, userdata, message):
		if message.topic == self.name:
			msg = json.loads(str(message.payload.decode('utf-8')))
			if not isinstance(msg, list):
				if not self.authorized:
					if msg:  											# msg == True
						self.authorized = True
						print('ID authorized by server')
					else:
						print('ID not authorized by server')
						self.client.unsubscribe(self.name)
						self.name = self.randomString(4)
						self.client.subscribe(self.name, 1)
						self.getAuth()
				else:
					print('[ERROR] message received not a list')
			else:
				self.msg = msg
		else:
			print('message that was not intended for you has been received')

	# general sending method
	def sendPublish(self, topic, message, qos):
		self.client.publish(topic, json.dumps(message), qos)

	def getAuth(self):
		self.sendPublish('AU', self.name, 1)

	# get a path by sending the name of the car as well as the RFID tag just read(GetPath)
	def getPath(self, tagId, msg):
		self.msg = msg
		self.sendPublish('GP', self.name + ',' + str(tagId), 1)
		while self.msg == 'get':
			pass
		return self.msg

	# confirm that you have arrived at the destination (ParkArrived)
	def arrived(self):
		self.sendPublish('PA', self.name, 1)
