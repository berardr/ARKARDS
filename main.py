#START OF ARKARDS PYTHON PLOTTER



import add_tag
import mqtt_sub
import pos_plotter

if __name__ == "__main__":
	print("Welcome to ARKARDS \nType \"add\" to add a tag to the database OR type \"plot\" to view a plot of active tags and anchors\nType \"exit\" to exit\n")
	
	while(1):
		mode = input("Enter mode: ")
		if mode == "add":
			print("add")
		elif mode == "plot":
			print("plot")
		elif mode == "exit":
			print("exit")
		else:
			print("invalid mode - try again")

