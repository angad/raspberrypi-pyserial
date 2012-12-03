import serial
import sys
import thread

sio = serial.Serial('/dev/ttyAMA0', 9600, stopbits=2)
sio.open()

print sio

transaction = []
item = {}
count = 0
barcode = ''
quantity = 1

def readSerialThread():
	print 'Starting serial thread'
	while True:
		try:
			byte = sio.read()
			# processInput(byte)
			sys.stdout.write(byte)
			sys.stdout.flush()
		except Exception as ex:
			print str(ex)

def processInput(byte):
	global count
	global item
	global transaction
	global quantity
	global barcode


	if byte == 'O' and sio.read() == 'P':
		item = {}
		transaction = []
		count = 0
		print "New Transaction"
	
	if byte == 'I' and sio.read() == 'T':
		count = count + 1
		item['quantity'] = quantity
		print "New Item"
	
	if byte == 'B' and sio.read() == 'A':
		for i in range(1,8):
			barcode = barcode + sio.read() 
		item['barcode'] = barcode
		print item
		print "Barcode received"

	if byte == 'Q' and sio.read() == 'A':
		quanitty = sio.read()
		item['quantity'] = quantity
		print "Quantity received"

def writeSerialThread(bytes):
	sio.write(bytes)

def main():
	hex = open('code.txt', 'r')
	code = hex.read()
	
	try:
		thread.start_new_thread(readSerialThread, ())
	except Exception as ex:
		print str(ex)

	sendHex = input('1 - send hex')
	if sendHex == 1:
		try:
			thread.start_new_thread(writeSerialThread, (code, ))
		except Exception as ex:
			print str(ex)

	while 1:
		pass

	
	
if __name__ == '__main__':
	main()
