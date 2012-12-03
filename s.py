import serial
import sys
import thread

sio = serial.Serial('/dev/ttyAMA0', 9600, stopbits=2)
sio.open()

print sio

def readSerialThread():
	print 'Starting serial thread'
	while True:
		try:
			byte = sio.read()
			processInput(byte)
			sys.stdout.write(byte)
			sys.stdout.flush()
		except Exception as ex:
			print str(ex)

def processInput(byte):
	if byte == 'O' and sio.read() == 'P':
		print "New Transaction"
	
	if byte == 'I' and sio.read() == 'T':
		print "New Item"
	
	if byte == 'B' and sio.read() == 'A':
		print "Barcode received"

	if byte == 'Q' and sio.read() == 'A':
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
