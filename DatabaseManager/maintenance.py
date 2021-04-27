#**********************************************************************************************
#										MAINTENANCE SCREEN
#
#		 The purpose of this file is to for the maintenance screen, handle functions like
#		adding users, and clearing the tags out, etc.
#**********************************************************************************************

from tkinter import *
from tkinter import messagebox
from tkinter import simpledialog
from database import *
from func_image import *
import pandas as pd
from pandastable import Table


# fonts
FONT_LARGE = ("Calibri", 24)
FONT_MEDIUM = ("Calibri", 16)
FONT_SMALL = ("Calibri", 12)


def start_maintenace(root, user, password):

	# hide the parent
	root.withdraw()

	# warn user, that db will be cleared, then prompt for password if they want to continue
	def clear_click():

			#disable the buttons
			button_disable()

			response = messagebox.askyesno("WARNING!","THIS WILL CLEAR TAGS, DO YOU WANT TO CONTINUE?")
			# yes is selected ask for password, used simple dialog for simplicity cant figure out how to center, who cares...
			if response == 1:

				# now check the password
				answer = simpledialog.askstring("Password", "Enter Password for : " + str(user), parent = admin_root, show = '*')

				#if the password is correct clear tags
				if answer == password:
					check = clear_tags(user, password)

					# if clear is works
					if check:
						image_clear()
						message_label.config(text = "CLEARING TAGS...", fg = "green")
						admin_root.after(1500, clear_text)

					else:
						message_label.config(text = "ERROR CLEARING TAGS...", fg = "red")
						admin_root.after(1500, clear_text)

				# othwerwise error
				else:
					button_normal()
					messagebox.showerror("ERROR!","INCORRECT PASSWORD!")
					
			button_normal()

			admin_root.focus_force()

	# unhide parent and close
	def home_click():
		root.deiconify()
		admin_root.destroy()

	# function for clicking backup, calls db function
	def backup_click():
		backup_db(user, password)
		message_label.config(text = "CREATING BACKUP...", fg = "green")
		admin_root.after(1500, clear_text)

	# function clicking add, creates child window
	def add_click():
		users_window(admin_root, user, password)


	# simple function for clearing text
	def clear_text():
		button_normal()
		message_label.config(text = "")

	def button_disable():
		clear_button.config(state = DISABLED)
		backup_button.config(state = DISABLED)
		add_button.config(state = DISABLED)
		home_button.config(state = DISABLED)

	def button_normal():
		clear_button.config(state = NORMAL)
		backup_button.config(state = NORMAL)
		add_button.config(state = NORMAL)
		home_button.config(state = NORMAL)

	#create the admin root
	admin_root = Toplevel(root)
	# set the title and icon
	admin_root.title("ARKARDS - MAINTENANCE")
	admin_root.iconbitmap("icon.ico")

	# set demintions for the window, also get the screen width and height for centering later
	admin_width = 1200
	admin_height = 720
	screen_width = admin_root.winfo_screenwidth()
	screen_height = admin_root.winfo_screenheight()

	# x and y variables for then placing the window onto the middle of the screen.
	x = (screen_width / 2) - (admin_width / 2)
	y = (screen_height / 2) - (admin_height / 2)

	# now set the geometry of the screen and center it
	admin_root.geometry(f'{admin_width}x{admin_height}+{int(x)}+{int(y)}')

	# incase window is force closed
	admin_root.bind("<Destroy>", lambda e: root.deiconify())

	# load the images
	logo_image = PhotoImage(file = "images/logo.png")
	add_image = PhotoImage(file = "images/users.png")
	clear_image =  PhotoImage(file = "images/clear.png")
	backup_image =  PhotoImage(file = "images/backup.png")
	home_image =  PhotoImage(file = "images/home.png")

	# frameS
	title_frame = Frame(admin_root)
	button_frame = Frame(admin_root)

	user_text = "Logged in: " + user

	# labels
	logo_label = Label(title_frame, image = logo_image, padx = 10, pady = 10)
	title_label = Label(title_frame,  text = "ARKARDS - Maintenance", font = FONT_LARGE, padx = 10, pady = 10)
	user_label = Label(admin_root, text = user_text, font = FONT_MEDIUM, pady = 10)
	message_label = Label(admin_root, text = "", font = FONT_MEDIUM, pady = 10)

	# buttons
	clear_button = Button(button_frame, image = clear_image, width = 175, height = 175, bd = 10, text = "Clear Tags", font = FONT_LARGE, compound = "top", command = clear_click)
	backup_button = Button(button_frame, image = backup_image, width = 175, height = 175, bd = 10, text = "Backup Tags", font = FONT_LARGE, compound = "top", command = backup_click)
	add_button = Button(button_frame, image = add_image, width = 175, height = 175,  bd = 10, text = "Users", font = FONT_LARGE, compound = "top", command = add_click)
	home_button = Button(button_frame, image = home_image, width = 175, height = 175,  bd = 10, text = "Main Screen", font = FONT_LARGE, compound = "top", command = home_click)

	# place the labels into the frame
	logo_label.grid(row = 0, column = 0)
	title_label.grid(row = 0, column = 1)


    # place buttons
	clear_button.grid(row = 0, column = 0, padx = 50, pady = 20)
	backup_button.grid(row = 0, column = 1, padx = 50, pady = 20)
	add_button.grid(row = 1, column = 0, padx = 50, pady = 20)
	home_button.grid(row = 1, column = 1, padx = 50, pady = 20)

	# pack the frame onto the screen
	title_frame.pack()
	button_frame.pack()

	# pack the user and message label
	user_label.pack()
	message_label.pack()

	# main loop
	admin_root.mainloop()


def users_window(root, user, password):

	# function for adding user, call child window
	def add_click():

		child_add(user_root, user, password, pt)

	# function for deleteing a selected user, will make it so foot can not be deleted.
	def delete_click():

		try:

			row = pt.getSelectedRow()
			user_selected = pt.model.getValueAt(row, 0)

			response = messagebox.askyesno("WARNING!","DO YOU WISH TO DELETE THIS USER?")

			if response == 1:

				if user_selected == "root":

					messagebox.showerror("ERROR!","ERROR: CAN NOT DELETE ROOT!")

				else:

					check = drop_user(user, password, user_selected)

					if not check:

						messagebox.showerror("ERROR!","ERROR CREATING USER")

					else:

						new_data = get_users(user, password)
						pt.model.df = new_data
						pt.redraw()
		except IndexError as err:
			pass


	# hide the parent
	root.withdraw()

	#create the admin root
	user_root = Toplevel(root)

	# set the title and icon
	user_root.title("ARKARDS - USERS")
	user_root.iconbitmap("icon.ico")

	# set demintions for the window, also get the screen width and height for centering later
	user_width = 900
	user_height = 900
	screen_width = user_root.winfo_screenwidth()
	screen_height = user_root.winfo_screenheight()

	# x and y variables for then placing the window onto the middle of the screen.
	x = (screen_width / 2) - (user_width / 2)
	y = (screen_height / 2) - (user_height / 2)

	# now set the geometry of the screen and center it
	user_root.geometry(f'{user_width}x{user_height}+{int(x)}+{int(y)}')

	# incase window is force closed
	user_root.bind("<Destroy>", lambda e: root.deiconify())

	# load the images
	add_image = PhotoImage(file = "images/add_user.png")
	delete_image =  PhotoImage(file = "images/delete.png")
	gear_image =  PhotoImage(file = "images/gear.png")

	# frame
	button_frame = Frame(user_root)

	# buttons
	delete_button = Button(button_frame, image = delete_image, width = 175, height = 175, bd = 10, text = "Delete User", font = FONT_LARGE, compound = "top", command = delete_click)
	add_button = Button(button_frame, image = add_image, width = 175, height = 175,  bd = 10, text = "Add User", font = FONT_LARGE, compound = "top", command = add_click)
	gear_button = Button(button_frame, image = gear_image, width = 175, height = 175,  bd = 10, text = "Maintenance", font = FONT_LARGE, compound = "top", command = user_root.destroy)


    # place buttons
	add_button.grid(row = 0, column = 0, padx = 50, pady = 20)
	delete_button.grid(row = 1, column = 0, padx = 50, pady = 20)
	gear_button.grid(row = 2, column = 0, padx = 50, pady = 20)

	table_frame = Frame(user_root)
	table_frame.pack(side = LEFT, fill = "both", expand = True)

	# pack button frame
	button_frame.pack(side =LEFT)

	# pandastable
	pt = Table(table_frame)
	data_frame = get_users(user, password)
	pt.model.df = data_frame
	pt.show()

	pt.unbind_all("<Tab>")
	pt.unbind_all("<Return>")

	# if user is not root then lock the add/remove users
	if user == "root":
		add_button.config(state = NORMAL)
		delete_button.config(state = NORMAL)

	else:
		add_button.config(state = DISABLED)
		delete_button.config(state = DISABLED)


	# main loop
	user_root.mainloop()


# fucnction for calling child window
def child_add(root, user, password, pt):

	# function for clicking the create button, checks passwords to make sure they match, then calls db funciton
	def add_click():

		# get values from the entry fields cast as strings
		user_value = str(user_entry.get())
		pass_value = str(pass_entry.get())
		check_pass_value = str(check_pass_entry.get())

		if pass_value == check_pass_value:

			user_check = add_user(user, password, user_value, pass_value)

			if user_check:

				message_label.config(text = "CREATING USER...", fg = "green")
				clear_entry()
				child_root.after(1500, clear_text)
				user_entry.focus_force()
				new_data = get_users(user, password)
				pt.model.df = new_data
				pt.redraw()

			else:

				message_label.config(text = "ERROR CREATING USER", fg = "red")
				child_root.after(1500, clear_text)

		# if passwords do not match error
		else:

			message_label.config(text = "PASSWORDS DO NOT MATCH!", fg = "red")
			child_root.after(1500, clear_text)

	# simple function for deleting the message label
	def clear_text():

		message_label.config(text = "")

	# simple function for clearing entry fields
	def clear_entry():

		user_entry.delete(0, END)
		pass_entry.delete(0, END)
		check_pass_entry.delete(0, END)

	#create the admin root
	child_root = Toplevel(root)
	# set the title and icon
	child_root.title("ARKARDS - CREATE USER")
	child_root.iconbitmap("icon.ico")

	# set demintions for the window, also get the screen width and height for centering later
	child_width = 600
	child_height = 350
	screen_width = root.winfo_screenwidth()
	screen_height = root.winfo_screenheight()

	# x and y variables for then placing the window onto the middle of the screen.
	x = (screen_width / 2) - (child_width / 2)
	y = (screen_height / 2) - (child_height / 2)

	# now set the geometry of the screen and center it
	child_root.geometry(f'{child_width}x{child_height}+{int(x)}+{int(y)}')

	# make the window a fixed size
	child_root.resizable(0,0)

	# create frames
	entry_frame = Frame(child_root)
	button_frame = Frame(child_root)

	# create labels
	title_label = Label(child_root, text = "CREATE NEW USER", font = FONT_LARGE, pady = 10)
	user_label = Label(entry_frame, text = "Username: ", font = FONT_SMALL)
	pass_label = Label(entry_frame, text = "Password: ", font = FONT_SMALL)
	check_pass_label = Label (entry_frame, text = "Re-enter Password: ", font = FONT_SMALL)
	message_label = Label(child_root, text = "", font = FONT_SMALL)

	# create entry boxes
	user_entry = Entry(entry_frame, width = 25, font = FONT_SMALL)
	pass_entry = Entry(entry_frame, width = 25, show = "*", font = FONT_SMALL)
	check_pass_entry = Entry(entry_frame, width = 25, show = "*", font = FONT_SMALL)

	# create buttons
	add_button = Button(button_frame, bd = 5, text = "Create User", font = FONT_SMALL, width = 10, command = add_click)
	cancel_button = Button(button_frame, bd = 5, text = "Cancel", font = FONT_SMALL, width = 10, command = child_root.destroy) # if pressed then exit application

	# place the labels and entry boxes into the frame
	user_label.grid(row = 0, column = 0, padx = 10, pady = 10)
	pass_label.grid(row = 1, column = 0, padx = 10, pady = 10)
	check_pass_label.grid(row = 2, column = 0, padx = 10, pady = 10)
	user_entry.grid(row = 0, column = 1, padx = 10, pady = 10)
	pass_entry.grid(row = 1, column = 1, padx = 10, pady = 10)
	check_pass_entry.grid(row = 2, column = 1, padx = 10, pady = 10)

	# place buttons onto the button frame
	add_button.grid(row = 0, column = 0, padx = 10, pady = 10)
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
	user_entry.bind("<Tab>", lambda e: pass_entry.focus_set())

	# if enter is pressed then focus on the password entry
	pass_entry.bind("<Return>", lambda e: check_pass_entry.focus_set())
	pass_entry.bind("<Tab>", lambda e: check_pass_entry.focus_set())

	#if enter is pressed same as clicking login button
	check_pass_entry.bind("<Return>", lambda e: add_click())
	check_pass_entry.bind("<Tab>", lambda e: user_entry.focus_set())

	child_root.mainloop()



#**********************************************************************************************
#						  		      END MAINTENANCE SCREEN
#**********************************************************************************************
