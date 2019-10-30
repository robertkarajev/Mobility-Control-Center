import mysql.connector as mysqlconn
import sshtunnel as ssh
import framework.timer as tm
import serial as se

username = 'xxx'
password = 'xxx'
host = 'xxx'

class Tag:
    def __init__(self):
        self.ser = se.Serial('COM3', 9600, timeout = 1)
        self.byte = 8

    def scan_tag(self):
        n = str(self.ser.read(self.byte))
        a,b,c = n.split("'")
        #print(n)
        if len(b) > 1:
            print(b)
            return str(b)


class SSHTunnel:
    def __init__(self, ssh_server_address, ssh_server_port, ssh_username, ssh_password, db_server_address, db_server_port):
        self.ssh_server_address = ssh_server_address
        self.ssh_server_port = ssh_server_port
        self.ssh_username = ssh_username
        self.ssh_password = ssh_password
        self.db_server_address = db_server_address
        self.db_server_port = db_server_port
        
    def createSSHTunnelForwarder(self):
        self.tunnelForwarder = ssh.SSHTunnelForwarder(ssh_address_or_host = (self.ssh_server_address, self.ssh_server_port),
                                             ssh_username = self.ssh_username,
                                             ssh_password = self.ssh_password,
                                             remote_bind_address = (self.db_server_address, self.db_server_port))
        return self.tunnelForwarder

    def startTunnel(self):
        self.tunnelForwarder.start()

    def closeTunnel(self):
        self.tunnelForwarder.stop()


class MySQLConnector:
    def __init__(self, db_username, db_password, db_name, db_local_address, db_local_port):
        self.db_username = db_username
        self.db_password = db_password
        self.db_name = db_name
        self.db_host = db_local_address
        self.db_port = db_local_port

    def startConnection(self):
        self.connection = mysqlconn.MySQLConnection(username = self.db_username,
                                         password = self.db_password,
                                         database = self.db_name,
                                         host = self.db_host,
                                         port = self.db_port)

    def closeConnection(self):
        self.connection.close()

    def insertLot(self):
        add_lot = ("INSERT INTO parking_lot "
                   "(id, is_space_available, number_of_blocks) "
                   "VALUES (%s, %s, %s)")
        lot_values = (1, 1, 30)
        self.connection.cursor().execute(add_lot, lot_values)
        self.connection.commit()

    def insertBlock(self):
        add_block = ("INSERT INTO parking_block "
                   "(id, parking_lot_id, number_of_spaces, available_spaces, is_block_full) "
                   "VALUES (%s, %s, %s, %s, %s)")
        block_values = ('A', 1, 99, 99, 0)
        self.connection.cursor().execute(add_block, block_values)
        self.connection.commit()

    def insertTag(self, tag):
        add_tag = ("INSERT INTO parking_space "
                   "(id, parking_block_id, space_number, availability) "
                   "VALUES (%s, %s, %s, %s)")
        tag_values = (tag, 'A', 0, 1)
        self.connection.cursor().execute(add_tag, tag_values)
        self.connection.commit()

#class that can read a scanned rfid tag
tag = Tag()

#realized SSHTunnel connection
timer = tm.Timer()
ssh_conn = SSHTunnel('xxx.xx.xxx.xxx', 22, username, password, host, 3306)
ssh_conn.createSSHTunnelForwarder()
ssh_conn.startTunnel()
timer.postpone(5, f'ssh connection status: {ssh_conn.tunnelForwarder.local_is_up(("xxx.xx.xxx.xxx", 22))} ')

#realized MySql connection
mysql_conn = MySQLConnector(username, password, 'smarterdam_parking', host, ssh_conn.tunnelForwarder.local_bind_port)
mysql_conn.startConnection()
print(f'db connection status: {mysql_conn.connection.is_connected()} \n')

#create parking lot and parking block
#mysql_conn.insertLot()
#mysql_conn.insertBlock()

isRunning = True
while isRunning:
    print('Scan your card: ')
    parking_space_id = tag.scan_tag()
    if parking_space_id == '29E5B718':
        isRunning = False
    elif parking_space_id != None:
        mysql_conn.insertTag(parking_space_id)

#closing all connections
print('\nabout to close connections')
mysql_conn.closeConnection()
ssh_conn.closeTunnel()





# #query for the database
# cursor.execute("show databases")

# for row in cursor.fetchall():
#     print ('result: ', row[0])