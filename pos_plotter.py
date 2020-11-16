#PLOT MQTT SUB POSITION

def start(nodeinfo_q):
	while(1):
		node_info = nodeinfo_q.get()
		while(node_info == 1):
			print("RECIEVED")
			print(nodeinfo_q.get())
