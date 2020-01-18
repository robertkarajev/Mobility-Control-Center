import serial
import time as tm

class SerialConnection:
    def __init__(self):
        self.serial_name = '/dev/ttyS0'
        self.baud_rate = 19200
        self.time_out = 1
        self.seperator = '/'
        self.remaining_msg = ''
        self.byte_limit = 10
        self.connection = serial.Serial('/dev/ttyS0',19200, 1)

    def serial_write(self,msg):
        self.connection.write(str(msg + self.seperator))

    def serial_read(self):
        msg = self.connection.read(self.byte_limit)
        incoming_msg = msg if not self.remaining_msg else (self.remaining_msg+msg)

        if incoming_msg:
            print(incoming_msg)
            if self.seperator in incoming_msg:
                self.filter_message(msg)
            else:
                self.remaining_msg = incoming_msg

    def filter_message(self,msg):
        filtered_msg, leftover_msg= msg.split(self.seperator)
        if leftover_msg:
            self.remaining_msg = leftover_msg
        else:
            self.remaining_msg = ''
        print(filtered_msg)

sc = SerialConnection()
while True:
    sc.serial_write('hello')
    sc.serial_read()
    tm.sleep(1)
