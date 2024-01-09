import RPi.GPIO as GPIO
import spidev
import time

# GPIO Setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(2, GPIO.OUT) # Red LED
GPIO.setup(3, GPIO.OUT) # Green LED
PWM = GPIO.PWM(3, 100) # PWM for green led

spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 1000000

while True:
    ch1 = 0
    raw1 = spi.xfer2([1, (ch1 << 4) | 0x80, 0])
    data1 = ((raw1[1]&3) << 8) | raw1[2]

    ch2 = 1
    raw2 = spi.xfer2([1, (ch2 << 4) | 0x80, 0])
    data2 = ((raw2[1] & 3) << 8) | raw2[2]

    cycle = (data2 / 1024) * 100
    PWM.start(cycle)

    if data1 > 1010:
        GPIO.output(2, GPIO.HIGH)
    elif data1 < 990:
        GPIO.output(2, GPIO.LOW)

    time.sleep(1)
