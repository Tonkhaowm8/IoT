import RPi.GPIO as GPIO
import time
import _thread

red = 2
blue = 3
green = 4
button = 17
blinkRed = 27
brightGreen = 13

GPIO.setmode(GPIO.BCM)
GPIO.setup(red, GPIO.OUT)
GPIO.setup(blue, GPIO.OUT)
GPIO.setup(green, GPIO.OUT)
GPIO.setup(button,GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(blinkRed, GPIO.OUT)
GPIO.setup(brightGreen, GPIO.OUT)

GPIO.output(red,0)
GPIO.output(blue,0)
GPIO.output(green,0)

press = 0
brightness = 0

def changeColor(ch):
	global press
	color = list(format(press % 8, '03b'))
	GPIO.output(red,int(color[0]))
	GPIO.output(blue,int(color[1]))
	GPIO.output(green,int(color[2]))
	press += 1
	time.sleep(0.1)

def thread1_def():
	pwm = GPIO.PWM(brightGreen, 100)
	pwm.start(0)
	global brightness
	while True:
		print(f"Brightness: {brightness} %")
		time.sleep(2)
		if brightness >= 100:
			brightness = 0
		else:
			brightness += 20
			time.sleep(0.1)
		pwm.ChangeDutyCycle(brightness)
	pwm.stop()

# Main Task
try:
	GPIO.add_event_detect(button, GPIO.RISING, callback=changeColor, bouncetime = 200)
	_thread.start_new_thread(thread1_def, ())
	while True:
		GPIO.output(blinkRed, GPIO.HIGH)
		time.sleep(0.1)
		GPIO.output(blinkRed, GPIO.LOW)
		time.sleep(1)
        

finally:
    # Cleanup
    GPIO.cleanup()
