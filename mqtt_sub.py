#MQTT SUBSCRIBER



import paho.mqtt.client as mqtt


def on_connect(client, userdata, flags, rc):

def on_message(client, userdata, msg):

def start(taginfo_q, startflag_q):
	client = mqtt.Client()
	client.on_connect = on_connect
	client.on_message = on_message
	host = "192.168.1.35"
	port = "1883"
	print("connecting to client...")
	client.connect(host, port, 60)
	print("succesful")



