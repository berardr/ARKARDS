#**********************************************************************************************
#										MAIN SCREEN
#
#		 function for starting the menu, accept the user and pass from the menu screen
#**********************************************************************************************
from tkinter import *
from database import *
from add_screen import *
from maintenance import *
from view import *

# fonts
FONT_LARGE = ("Calibri", 24)
FONT_MEDIUM = ("Calibri", 16)
FONT_SMALL = ("Calibri", 12)


def start_menu(user, password):

	# if the add button is clicked open the child window for the add screen
	def add_click():
		start_add(menu_root, user, password)

	# if the maintenance button is clicked open the child window for the maintenance screen
	def gear_click():
		start_maintenace(menu_root, user, password)

	# if the view button is clicked open the child window for the view screen
	def view_click():
		start_view(menu_root, user, password)



	#create the menu root
	menu_root = Tk()

	# set the title and icon
	menu_root.title("ARKARDS - MENU")
	menu_root.iconbitmap("icon.ico")

	# set demintions for the window, also get the screen width and height for centering later
	menu_width = 1200
	menu_height = 720
	screen_width = menu_root.winfo_screenwidth()
	screen_height = menu_root.winfo_screenheight()

	# x and y variables for then placing the window onto the middle of the screen.
	x = (screen_width / 2) - (menu_width / 2)
	y = (screen_height / 2) - (menu_height / 2)

	# now set the geometry of the screen and center it
	menu_root.geometry(f'{menu_width}x{menu_height}+{int(x)}+{int(y)}')

	# load the images
	logo_image = PhotoImage(file = "images/logo.png")
	add_image = PhotoImage(file = "images/add.png")
	view_image =  PhotoImage(file = "images/view.png")
	gear_image =  PhotoImage(file = "images/gear.png")
	exit_image =  PhotoImage(file = "images/exit.png")	

	# frameS
	title_frame = Frame(menu_root)
	button_frame = Frame(menu_root)

	# labels
	logo_label = Label(title_frame, image = logo_image, padx = 10, pady = 10)
	title_label = Label(title_frame,  text = "ARKARDS - Data Manager", font = FONT_LARGE, padx = 10, pady = 10)


	# buttons
	add_button = Button(button_frame, image = add_image, width = 175, height = 175, bd = 10, text = "Add Tag", font = FONT_LARGE, compound = "top", command = add_click)
	view_button = Button(button_frame, image = view_image, width = 175, height = 175, bd = 10, text = "View Tags", font = FONT_LARGE, compound = "top", command = view_click)
	gear_button = Button(button_frame, image = gear_image, width = 175, height = 175,  bd = 10, text = "Maintenance", font = FONT_LARGE, compound = "top", command = gear_click)
	exit_button = Button(button_frame, image = exit_image, width = 175, height = 175,  bd = 10, text = "Exit", font = FONT_LARGE, compound = "top", command = menu_root.destroy)

	# place the labels into the frame
	logo_label.grid(row = 0, column = 0)
	title_label.grid(row = 0, column = 1)

    # place buttons
	add_button.grid(row = 0, column = 0, padx = 50, pady = 20)
	view_button.grid(row = 0, column = 1, padx = 50, pady = 20)
	gear_button.grid(row = 1, column = 0, padx = 50, pady = 20)
	exit_button.grid(row = 1, column = 1, padx = 50, pady = 20)

	# pack the frame onto the screen
	title_frame.pack()
	button_frame.pack()

	# main loop
	menu_root.mainloop()

#**********************************************************************************************
#						  		      END MAIN SCREEN
#**********************************************************************************************

