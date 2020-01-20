import serial_connection as sc
import time as tm

serial = sc.SerialConnection(15) # Default byte limit is 10

while True:
    serial.serial_write("hello") # insert
    serial.serial_read()
    tm.sleep(1)