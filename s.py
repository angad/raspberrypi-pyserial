import serial
import sys
import thread
import os
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
			byte = sio.readline()
			# byte = sio.read()
			processInput(byte)
			# sys.stdout.write(byte)
			# sys.stdout.flush()
			print repr(byte)
		except Exception as ex:
			print str(ex)

def processInput(byte):
	global count
	global item
	global transaction
	global quantity
	global barcode
	
	command = ''
	barcode = ''
	
	if byte[0] == 'i' or  byte[0] == '_':
		line = byte[1:].partition(',')
		print line
		barcode = line[0]
		quantity = line[2]

		print "Barcode: " + barcode
		print "Quantity: " + quantity

		curl =  os.popen("curl -s --data 'barcode=%s' http://172.27.229.252/getPrice.php" % (barcode)).read()
		print repr(curl)
		curl.strip()
		sio.write(curl)

	#if byte == '_':
	#	transaction = []
	#	item = {}
	#	count = 0
	#	print "New Transaction!"
	

	#if byte == '!':
	

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
