import paho.mqtt.client as paho
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(2, GPIO.OUT) # Pin 2 R

broker = "kmitl.ddns.net"
port = 9001

def on_message(mosq, obj, msg):
	global message
	print(msg.payload.decode("utf-8"))
	message = msg.payload.decode("utf-8")
	if message == "on":
		GPIO.output(2, GPIO.HIGH)
	else:
		GPIO.output(2, GPIO.LOW)
	
def on_subscribe(mosq, obj, mid, granted_qos):
	print("Subscribed: " + str(mid) + " " + str(granted_qos))
	
def on_publish(client, userdata, result):
	print("data public \n")
	pass

client1 = paho.Client("Tonkhaow", transport = "websockets")
client1.username_pw_set( username = "kmitliot", password = "KMITL@iot1234")
client1.on_publish = on_publish
client1.on_subscribe = on_subscribe
client1.on_message = on_message

client1.connect(broker, port)
# ret = client1.publish("yourtopic", "on")

client1.subscribe("Tonkhaow", 0)
client1.loop_forever()
