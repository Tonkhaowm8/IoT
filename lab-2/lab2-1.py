import spidev
import time

# Setup
spi = spidev.SpiDev()
spi.open(0,0) # spi0, ce0
spi.max_speed_hz = 1000000

#Read
ch = 0
while True:
    raw = spi.xfer2([1, (ch<<4) | 0x80,0])
    data = ((raw[1]&3)<<8) | raw[2]
    print("ADC Output : " + str(data))
    vr2 = (3.3 * data)/10
    print("VR2 :" + str(vr2))
    time.sleep(1)
