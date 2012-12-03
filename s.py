import serial
import sys

sio = serial.Serial('/dev/ttyAMA0', 9600, stopbits=2)
sio.open()

print sio

while 1:
	try:
		byte = sio.readline()
		print byte
	except Exception as ex:
		print str(ex)


def readSerialThread():
	print 'Starting serial thread'
	while True:
		try:
			byte = sio.read()
			

def main():
	hex = open('code.txt', 'r')
	code = hex.read()
	print code
	
	
