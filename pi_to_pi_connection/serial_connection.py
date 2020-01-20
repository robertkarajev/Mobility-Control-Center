import serial
import time as tm
import logger as lg
'''
Reminder turnoff console in /boot/cmdline.txt by removing baudrate and console parameter
'''
logger = lg.Logger(1)

class SerialConnection:
    def __init__(self, byte_limit = 10):
        self.serial_name = '/dev/ttyS0'
        self.baud_rate = 19200
        self.seperator = '/'
        self.remaining_msg = ''
        self.byte_limit = byte_limit
        self.connection = serial.Serial(self.serial_name, self.baud_rate, timeout=1)
        logger.info("Port: ", self.connection.name," Baudrate: ", self.baud_rate," ByteLimit: ",self.byte_limit)

    def serial_write(self,msg):
        self.connection.write(str(msg + self.seperator).encode())
        logger.info("Message sent:", msg) 

    def serial_read(self):
        if not self.connection.is_open: 
            self.connection.open() # reopening the port to refresh the data output
        msg = self.connection.read(self.byte_limit)
        msg = msg.decode() if msg else ''
        incoming_msg = msg if not self.remaining_msg else (self.remaining_msg+msg)

        if len(incoming_msg) <= self.byte_limit:
            if self.seperator in incoming_msg:
                self.connection.close()                 # close connection to prevent any other data leaking in
                return self.filter_message(msg)
            else:
                self.remaining_msg = incoming_msg
        else:
            self.remaining_msg = ''

    def filter_message(self,msg):
        filtered_msg, leftover_msg= msg.split(self.seperator)
        if leftover_msg:
            self.remaining_msg = leftover_msg
        else:
            self.remaining_msg = ''
        logger.info("Message:",filtered_msg)
        
'''
sc = SerialConnection()
while True:
    sc.serial_write('hello')
    sc.serial_read()
    tm.sleep(1)
'''
