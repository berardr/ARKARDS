#**********************************************************************************************
#										LOGIN SCREEN
#
# This file contains the login screen, it accepts a user and password for the MYSQL DB
# If the credentials are valid, create DB if not already and then go to main screen
# maybe in futre add the host as an entry box?
#**********************************************************************************************


# import modules
from tkinter import *
from database import *
from menu import start_menu

# fonts
LARGE_FONT = ("Calibri", 24)
SMALL_FONT = ("Calibri", 16)


# this fucntion starts the login screen, creates all the widgets and places them on the screen
def start_login():

	# this fuctions is triggered when the user presses the login button
	# it will take the given username and password and search it againts the sql database
	# if a match is found then open the rest of the application, if not then prompt wrong user/pass
	def login_click():

		# get the entered values from the field, cast to string just incase
		user = str(user_entry.get())
		password = str(pass_entry.get())

		# check the info agaisnt the user table in the db, return true or false
		connection = start_db(user, password)

		# base on if true or false either error or open the app
		if connection:

			message_label.config(text = "SUCCESS!!!", fg = "green")
			login_root.after(1000, lambda : success(user, password))

		else:
			message_label.config(text = "USERNAME/PASSWORD ERROR", fg = "red")
			login_root.after(1000, clear_text)

	# simple function for clearing text in the message field after error
	def clear_text():
		message_label.config(text = "")

	# simple function for destroy the window and calling the menu 	
	def success(user, password):
		login_root.destroy()
		start_menu(user, password)

	# create root
	login_root = Tk()

	# set title of window and the icon
	login_root.title("ARKARDS - LOGIN")
	login_root.iconbitmap("icon.ico")

	# set demintions for the window, also get the screen width and height for centering later
	login_width = 600
	login_height = 320
	screen_width = login_root.winfo_screenwidth()
	screen_height = login_root.winfo_screenheight()

	# x and y variables for then placing the window onto the middle of the screen.
	x = (screen_width / 2) - (login_width / 2)
	y = (screen_height / 2) - (login_height / 2)

	# now set the geometry of the screen and center it
	login_root.geometry(f'{login_width}x{login_height}+{int(x)}+{int(y)}')

	# make the window a fixed size
	login_root.resizable(0,0)

	# create frames
	entry_frame = Frame(login_root)
	button_frame = Frame(login_root)

	# create labels
	title_label = Label(login_root, text = "ARKARDS DATA MANAGER LOGIN", font = LARGE_FONT, pady = 10)
	user_label = Label(entry_frame, text = "Username: ", font = SMALL_FONT)
	pass_label = Label(entry_frame, text = "Password: ", font = SMALL_FONT)
	message_label = Label(login_root, text = "", font = SMALL_FONT)

	# create entry boxes
	user_entry = Entry(entry_frame, width = 25, font = SMALL_FONT)
	pass_entry = Entry(entry_frame, width = 25, show = "*", font = SMALL_FONT)

	# create buttons
	login_button = Button(button_frame, bd = 5, text = "Login", font = SMALL_FONT, width = 10, command = login_click)
	cancel_button = Button(button_frame, bd = 5, text = "Cancel", font = SMALL_FONT, width = 10, command = login_root.destroy) # if pressed then exit application

	# place the labels and entry boxes into the frame
	user_label.grid(row = 0, column = 0, padx = 10, pady = 10)
	pass_label.grid(row = 1, column = 0, padx = 10, pady = 10)
	user_entry.grid(row = 0, column = 1, padx = 10, pady = 10)
	pass_entry.grid(row = 1, column = 1, padx = 10, pady = 10)

	# place buttons onto the button frame
	login_button.grid(row = 0, column = 0, padx = 10, pady = 10)
	cancel_button.grid(row = 0, column = 1, padx = 10, pady = 10)

	# pack the title label
	title_label.pack()

	# pack the frame onto the screen
	entry_frame.pack(pady = 10)

	# pack the button frame onto the screen
	button_frame.pack(pady = 10)

	# pack the message label onto the screen
	message_label.pack()

	# set focus on the user entry label
	user_entry.focus_set()

	# if enter is pressed then focus on the password entry
	user_entry.bind("<Return>", lambda e: pass_entry.focus_set()) 

	#if enter is pressed same as clicking login button
	pass_entry.bind("<Return>", lambda e: login_click())

	# window loop
	login_root.mainloop()

#**********************************************************************************************
#						  		      END LOGIN SCREEN
#**********************************************************************************************