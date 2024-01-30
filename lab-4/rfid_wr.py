import RPi.GPIO as GPIO
import MFRC522
import signal
import time
print
continue_reading = True
#----------------------------------------------------------------------

# Capture SIGINT for cleanup when the script is aborted
def end_read(signal, frame):
	global continue_reading
	print("Ctrl+C captured, ending read")
	continue_reading = False
	GPIO.cleanup()

#----------------------------------------------------------------------

# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)

GPIO.setmode(GPIO.BOARD)

# Create an object of the class MRFC522
MIFAREReader = MFRC522.MFRC522()

# Welcome message
print("Welcome to the MFRC522 data write")
print("Press Ctrl+C to stop")

# This loop keeps checking for chips. If one is near it will get the UID and authentication
while continue_reading:
	(status, TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
	
	if status == MIFAREReader.MI_OK:
		print("Card detected")
		
		(status, uid) = MIFAREReader.MFRC522_Anticoll()
		
		if status == MIFAREReader.MI_OK:
			
			name1 = "Siraphop        "
			name2 = "Mukdaphetcharat "
			data1 = bytes(name1, "ascii")
			data2 = bytes(name2, "ascii")
			
			print("Sector 8 & 9 looked like this: ")
			
			name1 = MIFAREReader.MFRC522_Readdata(8)
			name2 = MIFAREReader.MFRC522_Readdata(9)
			
			name1 = "".join(map(chr,name1))
			name2 = "".join(map(chr,name2))
			
			print(name1 + name2 + "\n")
			
			print("Write Sector 8 & 9 : ")
			
			MIFAREReader.MFRC522_Write(8, data1)
			MIFAREReader.MFRC522_Write(9, data2)
			
			print("Now look like this: ")
			
			name1 = MIFAREReader.MFRC522_Readdata(8)
			name1 = MIFAREReader.MFRC522_Readdata(9)
			
			name1 = "".join(map(chr,name1))
			name2 = "".join(map(chr,name2))
			
			print(name1 + name2 + "\n")
			
			MIFARE.MFRC522_StopCrypto1()
			
			continue_reading = False
		else:
			
			print("Authentication error")
