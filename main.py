#START OF ARKARDS PYTHON PLOTTER



import add_node
import mqtt_sub
import pos_plotter
import threading
import queue


start_flag = object()

if __name__ == "__main__":
	print("Welcome to ARKARDS \nType \"add\" to add a node to the database OR type \"plot\" to view a plot of active tags and anchors\nType \"exit\" to exit\n")

	while(1):
		mode = input("Enter mode: ")
		if mode == "add":

			mode = add_node.start()
		elif mode == "plot":


			nodeinfo_q = queue.Queue()
			startflag_q = queue.Queue()
			plot_t = threading.Thread(target=pos_plotter.start, args=(nodeinfo_q,))
			sub_t = threading.Thread(target=mqtt_sub.start, args=(nodeinfo_q,))  

			plot_t.start()
			sub_t.start()
			plot_t.join()
			sub_t.join()
			

		elif mode == "exit":
			print("exit")
		else:
			print("invalid mode - try again")

