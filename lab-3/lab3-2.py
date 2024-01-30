import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO

broker = "kmitl.ddns.net"
port = 9001

def on_message(client, usrdata, message):
	print("Receive : " + str(message.payload.decode()) + "\n");
	if (message.payload.decode() == "0") :
		client.publish("TonkhaowHome/LampSta", "0")
		GPIO.output(2, False)
	else:
		client.publish("TonkhaowHome/LampSta", "1")
		GPIO.output(2, True)
		
def on_connect(client, usedata, flags, rc):
	if rc == 0:
		print("Successfully Connected");
	else:
		print("Error");

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.OUT)

client = mqtt.Client(transport = "websockets")
client.username_pw_set(username = "kmitliot", password = "KMITL@iot1234")
client.on_connect = on_connect
client.on_message = on_message

client.connect(broker, port)
client.subscribe("TonkhaowHome/LampCmd", 0)
client.loop_forever();
