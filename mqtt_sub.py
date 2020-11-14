#MQTT SUBSCRIBER



import paho.mqtt.client as mqtt
import json

def on_connect(client, userdata, flags, rc):
	#SEND STARTFLAG TO PLOT
	print("connection succesful")
	client.subscribe("dwm/node/#")
	print(type(userdata[1]))


def on_message(client, userdata, msg):
	print(msg.topic + " "+ str(msg.payload))

#def load_tag_info():

def start(nodeinfo_q, startflag_q):

	#LOAD JSON FILE
	node_json_path = "/home/kali/Desktop/ARKARDS/node_ref.json"
	with open(node_json_path) as node_f:
		node_data = json.load(node_f)
	userdata_vars = [nodeinfo_q, startflag_q, node_data]
	print(type(userdata_vars[1]))
	client = mqtt.Client(userdata = userdata_vars)
	client.on_connect = on_connect
	client.on_message = on_message
	host = "192.168.1.35"
	port = 1883
	print("connecting to client...")
	client.connect(host, port, 60)
	client.loop_forever()



