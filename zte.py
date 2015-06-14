import serial
from curses import ascii
import time

def openModem(modem, time):
	print "Openning " + modem
	serialPort = serial.Serial(modem, 460800, timeout=5)
	if serialPort.isOpen():
		print "Modem opened."
		return serialPort
	else:
		print "Could not open modem"
		return -1

def closeModem(modem):
	if modem.isOpen():
		modem.close()
		print "Modem closed."
	else:
		print "Modem is not opened."

def checkModem(modem):
	modem.write("AT\r")
	modem.readline()
	status = modem.readline()
	if status.startswith("OK"):
		print "AT OK"
		return True
	else:
		return False
				

def setModemTextMode(modem):
	modem.write("AT+CMGF=1\r")
	modem.readline()
	status = modem.readline()
	if status.startswith("OK"):
		print "Modem set in text mode"
		return True
	else:
		return False

def sendSMS(modem, phoneNumber, text):
	modem.write('AT+CMGS="%s"\r' %phoneNumber)
	modem.write(text)
	modem.write(ascii.ctrl('z'))
	time.sleep(2)
	
	modem.readline()
	modem.readline()
	modem.readline()
	cmgi = modem.readline()
	modem.readline()
	modem.readline()
	status = modem.readline()
	if status.startswith("OK"):
		print "SMS sent."
		return True
	else:
		print "Error sending SMS"
		return False

def deleteSMS(modem, messageIndex):
	modem.write("AT+CMGD=%s\r" %messageIndex)
	modem.readline()
	status = modem.readline()

	if status.startswith("OK"):
		print "SMS deleted"
		return True
	else:
		return False

def readSMS(modem, messageIndex):
	modem.write("AT+CMGR=%s\r" %messageIndex)
	time.sleep(2)

	modem.readline()
	header = modem.readline()
	body = modem.readline()
	modem.readline()
	status = modem.readline()
	print status
	if status.startswith("OK"):
		print "SMS read."
		return body
	else:
		print "Error reading SMS"

def readLineFromModem(modem):
	return modem.readline()

def flushBuffer(modem):
	modem.readlines()

def getMessageIndex(newMessageString):
	newSMSIndicationParts = newMessageString.split(":")
	#print newSMSIndicationParts[1]
	messageIndex = newSMSIndicationParts[1].split(",")[1]
	#print messageIndex
	return messageIndex
