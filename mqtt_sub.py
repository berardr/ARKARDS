#MQTT SUBSCRIBER



import paho.mqtt.client as mqtt
import json
import re

def on_connect(client, userdata, flags, rc):
	#SEND STARTFLAG TO PLOT
	print("connection succesful")
	userdata[0].put(1)
	client.subscribe("dwm/node/#")
<<<<<<< HEAD

=======
	#userdata[1].put(1)
	#hello this is vasil removing penis
>>>>>>> 0d67b08f7f7ea66904161e8e970a1faa743f0fa6


def on_message(client, userdata, msg):
	print(msg.topic + " "+ str(msg.payload))

def on_disconnect(client, userdata, rc):
	print("DISCONNECTED")
	userdata[0].put(0)

def on_config_msg(client, userdata, msg):

	nodeinfo_q = userdata[0]
	node_data = userdata[1]
	config_msg = json.loads(msg.payload)
	ID = re.search("node/(.+?)/uplink/config", msg.topic).group(1)
	if ((ID in node_data) and (config_msg["configuration"]["label"] == node_data[ID]["label"])): 
		if(config_msg["configuration"]["nodeType"] == "ANCHOR"):
			node_data[ID]["loc"]["x"] = config_msg["configuration"]["anchor"]["position"]["x"]
			node_data[ID]["loc"]["y"] = config_msg["configuration"]["anchor"]["position"]["y"]
			node_data[ID]["loc"]["z"] = config_msg["configuration"]["anchor"]["position"]["z"]
			node_data[ID]["config"] = "True"
		else:
			node_data[ID]["config"] = "True"
	else:
		print("UNREGISTERED CONFIG MESSAGE: " + node_data[ID]["label"])
		print(node_data[ID])
		print(config_msg["configuration"]["label"])


def on_status_msg(client, userdata, msg):
	
	nodeinfo_q = userdata[0]
	node_data = userdata[1] 
	status_msg = json.loads(msg.payload)
	
	ID = re.search("node/(.+?)/uplink/status", msg.topic).group(1)
	if (ID in node_data):
		node_data[ID]["status"] = status_msg["present"]
		msg = [node_data[ID]["label"], 
			node_data[ID]["status"], 
			node_data[ID]["type"],
			node_data[ID]["loc"]["x"],
			node_data[ID]["loc"]["y"],
			node_data[ID]["loc"]["z"],
			node_data[ID]["loc"]["qual"]]
		nodeinfo_q.put(msg)

	else:
		print("UNREGISTERED STATUS MESSAGE: " + node_data[ID]["label"])
		print(node_data[ID])

def on_location_msg(client, userdata, msg):

	nodeinfo_q = userdata[0]
	node_data = userdata[1] 
	location_msg = json.loads(msg.payload)

	ID = re.search("node/(.+?)/uplink/location", msg.topic).group(1)
	if (ID in node_data):
		msg = [node_data[ID]["label"], 
			node_data[ID]["status"], 
			node_data[ID]["type"],
			location_msg["position"]["x"],
			location_msg["position"]["y"],
			location_msg["position"]["z"],
			location_msg["position"]["quality"]]
		nodeinfo_q.put(msg)

	else:
		print("UNREGISTERED LOCATION MESSAGE: " + node_data[ID]["label"])
		print(node_data[ID])


def start(nodeinfo_q):

	#LOAD JSON FILE
	nodeinfo_q.put(1)
	node_json_path = "/home/kali/Desktop/ARKARDS/node_ref.json"
	with open(node_json_path) as node_f:
		node_data = json.load(node_f)
	userdata_vars = [nodeinfo_q, node_data]
	client = mqtt.Client(userdata = userdata_vars)

	client.on_disconnect = on_disconnect
	client.message_callback_add("dwm/node/+/uplink/config", on_config_msg)
	client.message_callback_add("dwm/node/+/uplink/status", on_status_msg)
	client.message_callback_add("dwm/node/+/uplink/location", on_location_msg)
	client.on_message = on_message
	client.on_connect = on_connect
	host = "192.168.1.35"
	port = 1883
	print("connecting to client...")
	client.connect(host, port, 60)
	client.loop_forever()
