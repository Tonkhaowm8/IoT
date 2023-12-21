import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
from time import sleep # Import the sleep function from the time module

GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BCM) # Use physical pin numbering
GPIO.setup(2, GPIO.OUT) # Pin 2 R
GPIO.setup(3, GPIO.OUT) # Pin 3 G
GPIO.setup(4, GPIO.OUT) # Pin 4 B
GPIO.setup(17, GPIO.IN, pull_up_down = GPIO.PUD_DOWN) # Pin 17 Button

def changeColor(rgb):
    GPIO.output(2, 1 - int(rgb[0]))
    GPIO.output(3, 1 - int(rgb[1]))
    GPIO.output(4, 1 - int(rgb[2]))

buttonPressed = 0
isPressed = False
rgbVal = [0,0,0]

# Loop

while True:
    changeColor(rgbVal)
    if GPIO.input(17) == GPIO.HIGH:
        isPressed = True
        print("Button is pressed")
    sleep(0.5)
    
    if isPressed:
        rgbVal =list(format(buttonPressed % 8, '03b'))
        print(f"RGB: {rgbVal}")
        changeColor(rgbVal)
        isPressed = False
        buttonPressed += 1
    sleep(0.1)
