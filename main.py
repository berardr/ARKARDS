#START OF ARKARDS PYTHON PLOTTER



import add_tag
import mqtt_sub
import pos_plotter
import threading
import queue




if __name__ == "__main__":
	print("Welcome to ARKARDS \nType \"add\" to add a tag to the database OR type \"plot\" to view a plot of active tags and anchors\nType \"exit\" to exit\n")
	
	while(1):
		mode = input("Enter mode: ")
		if mode == "add":
			print("add")
			mode = add_tag.start()
		elif mode == "plot":
			print("plot")

			taginfo_q = queue.Queue()
			startflag_q = queue.Queue()
			plot_t = threading.Thread(target=pos_plotter.start, args=(taginfo_q, startflag_q,))
			sub_t = threading.Thread(target=mqtt_sub.start, args=(taginfo_q, startflag_q,))  

			plot_t.start()
			sub_t.start()


		elif mode == "exit":
			print("exit")
		else:
			print("invalid mode - try again")

