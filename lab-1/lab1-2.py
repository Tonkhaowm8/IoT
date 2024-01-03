import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
from time import sleep # Import the sleep function from the time module
import _thread # Import Thread

GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BCM) # Use physical pin numbering
GPIO.setup(2, GPIO.OUT) # Pin 2 R
GPIO.setup(3, GPIO.OUT) # Pin 3 G
GPIO.setup(4, GPIO.OUT) # Pin 4 B
GPIO.setup(17, GPIO.IN, pull_up_down = GPIO.PUD_DOWN) # Pin 17 Button
GPIO.setup(27, GPIO.OUT) # Pin 27, Red LED
GPIO.setup(13, GPIO.OUT) # Pin 13, Green LED (PWM1)

#--------------------------- Setup Code --------------------------------

buttonPressed = 0
rgbVal = [0,0,0]
brightness = 0

# Change Color Function
def changeColor(rgb):
    GPIO.output(2, 1 - int(rgb[0]))
    GPIO.output(3, 1 - int(rgb[1]))
    GPIO.output(4, 1 - int(rgb[2]))

# Function which is called when button pushed (From Lab 1.1)
def button_irq(ch):
	global buttonPressed
	rgbVal = list(format(buttonPressed % 8, '03b'))
	print(f"RGB: {rgbVal}")
	changeColor(rgbVal)
	buttonPressed += 1
	sleep(0.1)

# Function which tell what to do when thread start
def thread1_def():
	pwm = GPIO.PWM(13, 50) # Pin 13 (PWM0) at 50Hz frequency
	pwm.start(0) # Start brightness at 0%
	global brightness
	while True:
		print(f"Brightness Level At: {brightness}%")
		sleep(2)
		if brightness >= 100:
			brightness = 0
		else:
			brightness += 20
			sleep(0.1)
		pwm.ChangeDutyCycle(brightness) # Change the brightness of the LED
	pwm.stop() # Stop the pwm if the loop breaks

# Tell GPIO to activate button function when it detects the button is pressed
GPIO.add_event_detect(17, GPIO.RISING, callback=button_irq, bouncetime = 200)

#--------------------------- Main Task ---------------------------------

# Start the thread
_thread.start_new_thread(thread1_def, ())

# Loop
while True:
	
	# Tell LED to blink
    GPIO.output(27, GPIO.HIGH)
    sleep(0.1)
    GPIO.output(27, GPIO.LOW)
    sleep(1)
    
        
    
