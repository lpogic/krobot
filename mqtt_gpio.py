import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt
import time

GPIO.setmode(GPIO.BCM)
pwms = {}
outputs = {}

mqttBroker ="localhost"
client = mqtt.Client("Client")

def falling_edge_callback(channel):
	client.publish("gpio_edge", "falling/{channel}")

def rising_edge_callback(channel):
	client.publish("gpio_edge", "rising/{channel}")

def on_message(client, userdata, message):
	global outputs
	global pwms
	msg = str(message.payload.decode("utf-8"))
	print("received message: " ,str(msg))
	parts = msg.split("/")
	proc = parts[0]
	if proc == "output":
		for p in parts[1:]:
			pin = int(p)
			GPIO.setup(pin, GPIO.OUT)
			GPIO.output(pin, 0)
			outputs[pin] = 0
	elif proc == "high":
		for p in parts[1:]:
			pin = int(p)
			if pin not in outputs:
				GPIO.setup(pin, GPIO.OUT)
			GPIO.output(pin, 1)
			outputs[pin] = 1
	elif proc == "low":
		for p in parts[1:]:
			pin = int(p)
			if pin not in outputs:
				GPIO.setup(pin, GPIO.OUT)
			GPIO.output(pin, 0)
			outputs[pin] = 0
	elif proc == "pwm":
		duty = int(parts[1])
		freq = int(parts[2])
		for p in parts[3:]:
			pin = int(p)
			if pin not in outputs:
				GPIO.setup(pin, GPIO.OUT)
			if pin not in pwms:
				pwms[pin] = GPIO.PWM(pin, freq)
				pwms[pin].start(duty)
			else:
				pwms[pin].ChangeFrequency(freq)
				pwms[pin].ChangeDutyCycle(duty)
	elif proc == "input":
		for p in parts[1:]:
			pin = int(p)
			GPIO.setup(pin, GPIO.IN)
			GPIO.add_event_detect(pin, GPIO.RISING, callback=rising_edge_callback, bouncetime=100)
	elif proc == "pullup":
		for p in parts[1:]:
			pin = int(p)
			GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
			GPIO.remove_event_detect(pin)
			GPIO.add_event_detect(pin, GPIO.RISING, callback=rising_edge_callback, bouncetime=100)
	elif proc == "pulldown":
		for pin in parts[1:]:
			pin = int(p)
			GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
			GPIO.remove_event_detect(pin)
			GPIO.add_event_detect(pin, GPIO.RISING, callback=rising_edge_callback, bouncetime=100)
		
def log(client, userdata, level, buff):
	with open("log.log", "a") as file:
		file.write(f"{userdata}:::{level}:::{buff}\n")

#client.on_log = log
client.connect(mqttBroker, 5678) 

client.subscribe("gpio")
client.on_message = on_message

try:
	client.loop_forever()
except KeyboardInterrupt:
	print(" Bye Bye!")
finally:
	GPIO.cleanup()
