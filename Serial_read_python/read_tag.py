import serial as se

ser = se.Serial('COM6', 9600, timeout = 1)
#file = open("rfid_tags.txt","a")

byte = 8

def scan_tag():
	n = str(ser.read(byte))
	a,b,c = n.split("'")
	#print(n)
	if len(b) > 1:
		print(b)
		return str(b)

def run():
	print("Please scan your card: ")
	while True:
		scan_tag()
		if(scan_tag()
run()