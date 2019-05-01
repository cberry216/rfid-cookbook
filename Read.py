import RPi.GPIO as GPIO
import MFRC522
import signal
import time

from interface import Interface
 
continue_reading = True
 
# Capture SIGINT for cleanup when the script is aborted
def end_read(signal,frame):
    global continue_reading
    print ("Ctrl+C captured, ending read.")
    continue_reading = False
    GPIO.cleanup()
    return
 
# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)

# Set mode to board
GPIO.setmode(GPIO.BOARD)
 
# Create an object of the class MFRC522
MIFAREReader = MFRC522.MFRC522()

# Setup RFID-Python Interface
interface = Interface()

# Welcome message
print ("Welcome to the RFID Cookbook")
print ("Start scanning your recipe cards to get started")
 
# This loop keeps checking for chips. If one is near it will get the UID and authenticate
while continue_reading:
    
    # Scan for cards    
    (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
 
    # If a card is found
    if status == MIFAREReader.MI_OK:
        print ("Card detected")
    
    # Get the UID of the card
    (status,uid) = MIFAREReader.MFRC522_Anticoll()
 
    # If we have the UID, continue
    if status == MIFAREReader.MI_OK:
 
        # Print UID
        print ("Card read UID: "+str(uid[0])+","+str(uid[1])+","+str(uid[2])+","+str(uid[3])+','+str(uid[4]))  
        
	# This is the default key for authentication
        key = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]
        
        # Select the scanned tag
        MIFAREReader.MFRC522_SelectTag(uid)
        
	interface.process_rfid(uid)	

	time.sleep(3)

        #ENTER Your Card UID here
        #my_uid = [180,92,97,19,154]
        
        #Configure LED Output Pin
        #LED = 18
        #GPIO.setup(LED, GPIO.OUT)
        #GPIO.output(LED, GPIO.LOW)
        
        #Check to see if card UID read matches your card UID
        #if uid == my_uid:                #Open the Doggy Door if matching UIDs
        #    print("Access Granted")
        #    GPIO.output(LED, GPIO.HIGH)  #Turn on LED
        #    time.sleep(5)                #Wait 5 Seconds
        #    GPIO.output(LED, GPIO.LOW)   #Turn off LED
            
        #else:                            #Don't open if UIDs don't match
        #    print("Access Denied, YOU SHALL NOT PASS!")
