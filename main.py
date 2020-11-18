#START OF ARKARDS PYTHON PLOTTER



import add_node
import mqtt_sub
import pos_plotter
import threading
import queue
import signal
import sys



if __name__ == "__main__":

	print("Welcome to ARKARDS \nType \"edit\" to edit the database OR type \"plot\" to view a plot of active tags and anchors\nType \"exit\" to exit")

	while(1):
		try:
			nodeinfo_q = queue.Queue()
			startflag_q = queue.Queue()
			mode = input("\nEnter mode: ")
			if mode == "edit":

				mode = add_node.start()
			elif mode == "plot":

				plot_t = threading.Thread(target=pos_plotter.start, args=(nodeinfo_q,))
				sub_t = threading.Thread(target=mqtt_sub.start, args=(nodeinfo_q,))

				plot_t.start()
				sub_t.start()
				plot_t.join()
				sub_t.join()


			elif mode == "exit":
				print("EXITING")
				sys.exit(0)
			else:
				print("invalid mode - try again")
		except KeyboardInterrupt:
			nodeinfo_q.put("OFF")
