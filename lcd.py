import serial
import sys
import thread
import os

from time import sleep

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
			# byte = sio.readline()
			byte = sio.read()
			# processInput(byte)
			sys.stdout.write(byte)
			sys.stdout.flush()
			# print repr(byte)
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
	
	if byte[0] == '1' or  byte[0] == '_':
		line = byte[1:].partition(',')
		print line
		barcode = line[0]
		quantity = line[2]

		print "Barcode: " + barcode
		print "Quantity: " + quantity

		curl =  os.popen("curl -s --data 'barcode=%s' http://127.0.1.1/getPrice.php" % (barcode)).read()
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

	# sio.write('1')

	sendHex = input('1 - send hex')
	if sendHex == 1:
		try:
			thread.start_new_thread(writeSerialThread, (code, ))
		except Exception as ex:
			print str(ex)

	getinput = raw_input("sup!")
	sio.write(getinput)

	byte = sio.read()
	if byte == '1':
		curl = os.popen("curl -s --data 'ID=1' http://127.0.1.1/lcd.php").read()
		curl = curl.strip()
		print repr(curl)
	
	curl = curl.rsplit(',')
	print curl


	maxlen = 16
	curr = 0
	for i in curl[0]:
		curr = curr + 1
		if curr == maxlen: 
			break
		sleep(0.1)
		sio.write(i)
	
	for i in range(1,25):
		sleep(0.1)
		sio.write('0')

	sleep(0.1)	
	sio.write('Q')
	sleep(0.1)
	sio.write(':')
	
	for i in curl[1]:
		sleep(0.1)
		sio.write(i)

	sleep(0.1)	
	sio.write('P')
	sleep(0.1)
	sio.write(':')
	
	for i in curl[2]:
		sleep(0.1)
		sio.write(i)

	sleep(0.1)
	sio.write('$')
		
	#sleep(1)
	#sio.write('1')
	#sleep(1)
	#sio.write('2')
	#sleep(1)
	#sio.write('3')
	#sleep(1)
	# sio.write('1')	

	while 1:
		pass

	
	
if __name__ == '__main__':
	main()
