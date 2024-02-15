import RPi.GPIO as GPIO
import MFRC522
import signal
import time
import sys
from urllib.request import urlopen
print
continue_reading = True

# Capture SIGINT for cleanup when the script is aborted
def end_read(signal,frame):
    global continue_reading
    print("Ctrl+C captured, ending read")
    continue_reading = False
    GPIO.cleanup()
    
# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)

GPIO.setmode(GPIO.BOARD)

#Create an object of the class MFRC522
MIFAREReader = MFRC522.MFRC522()

print ("Welcome to the MFRC522 data write")
print ("Press Ctrl-C to stop")

while continue_reading:
    
    # Scan for card
    (status, Tagtype) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
    
    # If a card is found
    if status == MIFAREReader.MI_OK:
        print("Card detected")
        
    (status, uid) = MIFAREReader.MFRC522_Anticoll()
    
    if status == MIFAREReader.MI_OK:
        print("Card read UID: ", uid[0], ":", uid[1], ":",uid[2],":",uid[3])
        
        key = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]
        
        MIFAREReader.MFRC522_SelectTag(uid)
        
        status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, 8, key, uid)
        
        if status == MIFAREReader.MI_OK:
            data1 = MIFAREReader.MFRC522_Readdata(8)
            data2 = MIFAREReader.MFRC522_Readdata(8)
            name = "".join(map(chr,data1))
            fname = "".join(map(chr,data2))
        
            
            res="http://kmitl.ddns.net/iot/Siraphop/insert.php?name="+name+"_"+fname
            print(name)
            
            response=urlopen(res)
            
            if (response.read().decode('utf-8')=="1"):
                print("success")
            
            MIFAREReader.MFRC522_StopCrypto1()
        else:
            print("Authentication error")
            
        time.sleep(1)