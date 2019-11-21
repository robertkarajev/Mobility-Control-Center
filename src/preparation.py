import mysql.connector as mysqlconn
import modules.timer as tm
import modules.services as sv
import modules.testservices as tsv

username = ''
password = ''
server_address = ''

#SSHTunnel connection
timer = tm.Timer()
ssh_conn = tsv.SSHTunnel(server_address, 22, username, password, 'localhost', 3306)
ssh_conn.createSSHTunnelForwarder()
ssh_conn.startTunnel()
timer.postpone(5, f'ssh connection status: {ssh_conn.tunnelForwarder.local_is_up((server_address, 22))} ')

#MySql connection
mysql_conn = sv.MySQLConnector(username, password, 'smarterdam_parking', 'localhost', ssh_conn.tunnelForwarder.local_bind_port)
mysql_conn.startConnection()
print(f'db connection status: {mysql_conn.connection.is_connected()} \n')

#Wiegand scanner
rfid_scanner = sv.Wiegand()

#create parking lot and parking block
# mysql_conn.insertLot('ModelParking', 1, 0)
# mysql_conn.insertWing('NORTH', 3, 3, 0, 'ModelParking')
# mysql_conn.insertWing('EAST', 4, 4, 0, 'ModelParking')
# mysql_conn.insertWing('WEST', 4, 4, 0, 'ModelParking')
# mysql_conn.insertWing('SOUTH', 3, 3, 0, 'ModelParking')
# mysql_conn.insertWing('CENTER', 4, 4, 0, 'ModelParking')

#logic
isRunning = True
while isRunning:
	rfid_tag = rfid_scanner.run()
	if rfid_tag == '5b35866e':
		print('Scanned card: ', rfid_tag)
		isRunning = False
	elif rfid_tag != None:
		print('Scanned card: ', rfid_tag)
		space_number = int(input('Space number: '))
		location = str(input('Location: '))
		id_parking_wing = str(input('Parking wing: '))
		print('Rfid parking space tag: ', rfid_tag)
		print(f'Record: {space_number}, {rfid_tag}, {location}, {1}, {id_parking_wing}')
		mysql_conn.insertSpace(space_number, rfid_tag, location, 1, id_parking_wing)

#closing all connections
print('\nabout to close connections')
mysql_conn.closeConnection()
ssh_conn.closeTunnel()