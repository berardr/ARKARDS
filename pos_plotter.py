#PLOT MQTT SUB POSITION

def start(nodeinfo_q):
	node_info = nodeinfo_q.get()
	while(node_info == "ON"):
		data = nodeinfo_q.get()
		if(data is "OFF"):
			break
		else:
			print(data)
		
