
#**********************************************************************************************
#										ADD SCREEN
#
# this function is for adding a tag into the MySQL db. This will be a child window to the main
# screen and will accepnt a root as a parameter, in this case the menu root
#**********************************************************************************************

# import modules
from tkinter import *
from database import *
from tkinter import filedialog
from func_image import *

# fonts
FONT_LARGE = ("Calibri", 24)
FONT_MEDIUM = ("Calibri", 16)
FONT_SMALL = ("Calibri", 12)


def start_add(root, user, password):
	# hide the parent
	root.withdraw()

	# function for browsing to open an image file, currently only png, jpeg, and bitmap files are shown
	def browse():

		add_root.filename = filedialog.askopenfilename(initialdir = "/", title = "Select An Image", filetypes = (("png files", "*.png"), ("jpeg files","*.jp*"), ("bitmap files", "*.bmp")))
		image_label.config(text = add_root.filename)
		add_root.focus_force() # bring the add screen to focus when exiting the dialog window

	# simple function for clearing text in the message field after error
	def clear_text():
		message_label.config(text = "")

	# fuction for clicking the add button
	def add_click():

		# get the values from the entry boxs
		first_value = str(first_entry.get())
		last_value = str(last_entry.get())
		height_value = str(height_entry.get())
		weight_value = str(weight_entry.get())
		sex_value = str(sex_entry.get())
		tag_value = str(tag_entry.get())
		pic_value = str(image_label.cget("text"))

		# make sure everthying is filled out
		if (len(first_value) == 0 or len(last_value) == 0 or len(height_value) == 0 or len(weight_value) == 0 or len(sex_value) == 0 or len(tag_value) == 0 or len(pic_value) == 0):

			message_label.config(text = "MISSING ENTRY FIELD!", fg = "red")
			add_root.after(1000, clear_text)

		else:
			# check to make sure the tag is not already added
			duplicate = check_tag(user, password, tag_value)

			# if the tag is not there then we will save the image, and attempt to add the tag
			if not duplicate:

				# call the image function, copy image and get new path
				path = image_open(pic_value, tag_value)

				# call add function
				check = add_tag(user, password, tag_value, first_value, last_value, height_value, weight_value, sex_value, path)

				if check :
					message_label.config(text = "TAG SUCCESSFULLY ADDED!", fg = "green")
					clear_entry()
					add_root.after(1000, clear_text)
				else:
					message_label.config(text = "ERROR ADDING TAG!", fg = "red")
					add_root.after(1000, clear_text)

			# if the tag is already added, error
			else:
					message_label.config(text = "TAG ALREAY EXISTS!", fg = "red")
					add_root.after(1000, clear_text)

	# simple function for clearing the entry fields
	def clear_entry():
		first_entry.delete(0, END)
		last_entry.delete(0, END)
		height_entry.delete(0, END)
		weight_entry.delete(0, END)
		sex_entry.delete(0, END)
		tag_entry.delete(0, END)
		image_label.config(text = "")

	# create child window
	add_root = Toplevel(root)

	# incase window is force closed
	add_root.bind("<Destroy>", lambda e: root.deiconify())

	# set the title and icon
	add_root.title("ARKARDS - ADD")
	add_root.iconbitmap("icon.ico")

	# window demenisons
	add_width = 500
	add_height = 700

	# window width and height of the splash screen and screen
	screen_width = add_root.winfo_screenwidth()
	screen_height =add_root.winfo_screenheight()

	# x and y variables for centering the screen
	x = (screen_width / 2) - (add_width / 2)
	y = (screen_height / 2) - (add_height / 2)

	# adjust the splash screen width and height and then center
	add_root.geometry(f'{add_width}x{add_height}+{int(x)}+{int(y)}')

	# make the window a fixed size
	add_root.resizable(0,0)

	# title and message labels
	title_label = Label(add_root, text = "Add Tag to DB", font = FONT_LARGE, pady = 10)
	message_label = Label(add_root, text = "", font = FONT_MEDIUM, pady = 10)

	# frames
	entry_frame = Frame(add_root)
	button_frame = Frame(add_root)

	# labels for entry
	tag_label = Label(entry_frame, text = "Tag #:", font = FONT_SMALL, pady = 10)
	first_label = Label(entry_frame, text = "First Name:", font = FONT_SMALL, pady = 10)
	last_label = Label(entry_frame, text = "Last Name:", font = FONT_SMALL, pady = 10)
	height_label = Label(entry_frame, text = "Height:", font = FONT_SMALL, pady = 10)
	weight_label = Label(entry_frame, text = "Weight:", font = FONT_SMALL, pady = 10)
	sex_label = Label(entry_frame, text = "Sex:", font = FONT_SMALL, pady = 10)
	image_label = Label(entry_frame, pady = 10, wraplength = 400, justify = CENTER )

	# entry fields for the information
	tag_entry = Entry(entry_frame, width = 20, font = FONT_SMALL)
	first_entry = Entry(entry_frame, width = 20, font = FONT_SMALL)
	last_entry = Entry(entry_frame, width = 20, font = FONT_SMALL)
	height_entry = Entry(entry_frame, width = 20, font = FONT_SMALL)
	weight_entry = Entry(entry_frame, width = 20, font = FONT_SMALL)
	sex_entry = Entry(entry_frame, width = 20, font = FONT_SMALL)

	# buttons
	upload_button = Button(entry_frame, bd = 3, text = "Upload Image", font = FONT_SMALL, width = 15, command = browse)
	add_button = Button(button_frame, bd = 5, text = "Add", font = FONT_SMALL, width = 10, command = add_click)
	cancel_button = Button(button_frame, bd = 5, text = "Cancel", font = FONT_SMALL, width = 10, command = add_root.destroy) # if pressed then exit application

	# place labels into the frame
	tag_label.grid(row = 0, column = 0, padx = 10, pady = 10)
	first_label.grid(row = 1, column = 0, padx = 10, pady = 10)
	last_label.grid(row = 2, column = 0, padx = 10, pady = 10)
	height_label.grid(row = 3, column = 0, padx = 10, pady = 10)
	weight_label.grid(row = 4, column = 0, padx = 10, pady = 10)
	sex_label.grid(row = 5, column = 0, padx = 10, pady = 10)
	upload_button.grid(row = 6, column = 0, columnspan = 2, padx = 10, pady = 10)
	image_label.grid(row = 7, column = 0,columnspan = 2, padx = 10, pady = 5)

	# place the entry boxes into the frame
	tag_entry.grid(row = 0, column = 1, padx = 10, pady = 10)
	first_entry.grid(row = 1, column = 1, padx = 10, pady = 10)
	last_entry.grid(row = 2, column = 1, padx = 10, pady = 10)
	height_entry.grid(row = 3, column = 1, padx = 10, pady = 10)
	weight_entry.grid(row = 4, column = 1, padx = 10, pady = 10)
	sex_entry.grid(row = 5, column = 1, padx = 10, pady = 10)

	# place buttons to button frame
	add_button.grid(row = 0, column = 0, padx = 10, pady = 10)
	cancel_button.grid(row = 0, column = 1, padx = 10, pady = 10)

	# foucs on first box
	tag_entry.focus_set()

	# pack everything
	title_label.pack()
	entry_frame.pack()
	button_frame.pack()
	message_label.pack()

	# if enter or tab is pressed change focus
	tag_entry.bind("<Return>", lambda e: first_entry.focus_set())
	tag_entry.bind("<Tab>", lambda e: first_entry.focus_set())

	first_entry.bind("<Return>", lambda e: last_entry.focus_set())
	first_entry.bind("<Tab>", lambda e: last_entry.focus_set())

	last_entry.bind("<Return>", lambda e: height_entry.focus_set())
	last_entry.bind("<Tab>", lambda e: height_entry.focus_set())

	height_entry.bind("<Return>", lambda e: weight_entry.focus_set())
	height_entry.bind("<Tab>", lambda e: weight_entry.focus_set())

	weight_entry.bind("<Return>", lambda e: sex_entry.focus_set())
	weight_entry.bind("<Tab>", lambda e: sex_entry.focus_set())

	sex_entry.bind("<Return>", lambda e: tag_entry.focus_set())
	sex_entry.bind("<Tab>", lambda e: tag_entry.focus_set())



	add_root.mainloop()


#**********************************************************************************************
#						  		      END ADD SCREEN
#**********************************************************************************************
