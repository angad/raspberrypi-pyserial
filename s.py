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

cmd = ''
def readSerialThread():
	global cmd
	print 'Starting serial thread'
	while True:
		try:
			# byte = sio.readline()
			byte = sio.read()
			if byte != '\x08' and byte != 'n' and byte != '_':
				cmd = cmd + byte
			if byte == '\n':
				cmd = ''
			if byte == '_':
				newTransaction()
			if byte == 'n':
				print cmd
				anItem = cmd.rsplit(',')
				addNewItem(anItem[0], anItem[1])
				# processInput(cmd)
				cmd = ''
			if byte == 't':
				doneTransaction()
			sys.stdout.write(byte)
			sys.stdout.flush()
			#print repr(byte)
		except Exception as ex:
			print str(ex)


def newTransaction():
	global transaction
	global item
	global count
	
	transaction = []
	item = {}
	count = 0


def addNewItem(barcode, quantity):
	global item
	global transaction
	global count
	
	item = {}
	item['barcode'] = barcode
	item['quantity'] = quantity
	print item
	transaction.append(item)
	# transaction[count] = item
	count = count + 1

	# get price
	curl =  os.popen("curl -s --data 'barcode=%s' http://127.0.1.1/getPrice.php" % (barcode)).read()
	print repr(curl)
	curl.strip()
	sio.write(curl)
	sio.write('$')
	

def doneTransaction():
	# do curl request to add item to transaction
	print "Done transaction!"
	print transaction
	curlstr = ''
	for i in transaction:
		curlstr = curlstr + i['barcode'] + ',' + i['quantity'] + '|'
	curlstr = curlstr[0:len(curlstr)-1]

	curl = os.popen("curl -s --data 'arr=%s' http://127.0.1.1/checkout.php" % (curlstr)).read()
	print repr(curl)
	curl.strip()
	sio.write(curl)
	sio.write('$')
	#pass


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
