#**********************************************************************************************
#										VIEW SCREEN
#
#		 The purpose of this file is to view the current tags inside the database.
#**********************************************************************************************

from tkinter import *
from tkinter import messagebox
from database import *
from func_image import *
import pandas as pd
from pandastable import Table

# fonts
FONT_LARGE = ("Calibri", 24)
FONT_MEDIUM = ("Calibri", 16)
FONT_SMALL = ("Calibri", 12)

# start the view screen
def start_view(root, user, password):

	# function for deleting an entry
	def delete_click():

		try:

			row = pt.getSelectedRow()
			tag_selected = pt.model.getValueAt(row, 0)
			button_disable()

			response = messagebox.askyesno("WARNING!","DO YOU WISH TO DELETE THIS TAG?")

			if response == 1:
				

				check = drop_tag(user, password, tag_selected)

				if not check:

					messagebox.showerror("ERROR!","ERROR DELETING TAG")
					button_normal()

				else:

					new_data = get_tags(user, password)
					pt.model.df = new_data
					pt.redraw()
					button_normal()
		except IndexError as err:
			pass

		button_normal()

	# function for viewing the picture
	def view_click():

		try:

			row = pt.getSelectedRow()
			path_selected = pt.model.getValueAt(row, 6)

			# create root
			child_root = Toplevel(view_root)

			# set title of window and the icon
			child_root.title("ARKARDS - " + str(path_selected))
			child_root.iconbitmap("icon.ico")

			# set demintions for the window, also get the screen width and height for centering later
			child_width = 256
			child_height = 256
			screen_width = child_root.winfo_screenwidth()
			screen_height = child_root.winfo_screenheight()

			# x and y variables for then placing the window onto the middle of the screen.
			x = (screen_width / 2) - (child_width / 2)
			y = (screen_height / 2) - (child_height / 2)

			# now set the geometry of the screen and center it
			child_root.geometry(f'{child_width}x{child_height}+{int(x)}+{int(y)}')

			# make the window a fixed size
			child_root.resizable(0,0)

			img = image_view(path_selected)

			image_label = Label(child_root, image = img)

			image_label.pack(expand = True)

			button_disable()

			child_root.bind("<Destroy>", lambda e: button_normal())

			child_root.mainloop()

		except IndexError as err:
			pass

	def button_disable():
		view_button.config(state = DISABLED)
		delete_button.config(state = DISABLED)

	def button_normal():
		view_button.config(state = NORMAL)
		delete_button.config(state = NORMAL)

	# hide the parent window
	root.withdraw()

	#create the view root
	view_root = Toplevel(root)
	# set the title and icon
	view_root.title("ARKARDS - VIEW")
	view_root.iconbitmap("icon.ico")

	# set demintions for the window, also get the screen width and height for centering later
	view_width = 1200
	view_height = 720
	screen_width = view_root.winfo_screenwidth()
	screen_height = view_root.winfo_screenheight()

	# x and y variables for then placing the window onto the middle of the screen.
	x = (screen_width / 2) - (view_width / 2)
	y = (screen_height / 2) - (view_height / 2)

	# now set the geometry of the screen and center it
	view_root.geometry(f'{view_width}x{view_height}+{int(x)}+{int(y)}')

	# incase window is force closed
	view_root.bind("<Destroy>", lambda e: root.deiconify())

	# load the images
	view_image = PhotoImage(file = "images/magnify.png")
	delete_image =  PhotoImage(file = "images/delete.png")
	home_image =  PhotoImage(file = "images/home.png")	

	# frame
	button_frame = Frame(view_root)

	# buttons
	delete_button = Button(button_frame, image = delete_image, width = 175, height = 175, bd = 10, text = "Delete Tag", font = FONT_LARGE, compound = "top", command = delete_click)
	view_button = Button(button_frame, image = view_image, width = 175, height = 175,  bd = 10, text = "View Tag", font = FONT_LARGE, compound = "top", command = view_click)
	home_button = Button(button_frame, image = home_image, width = 175, height = 175,  bd = 10, text = "Main Screen", font = FONT_LARGE, compound = "top", command = view_root.destroy)


    # place buttons
	view_button.grid(row = 0, column = 0, padx = 50, pady = 20)
	delete_button.grid(row = 0, column = 1, padx = 50, pady = 20)
	home_button.grid(row = 0, column = 2, padx = 50, pady = 20)

	table_frame = Frame(view_root)
	table_frame.pack(fill = "both", expand = True)

	# pack button frame
	button_frame.pack()

	# pandastable
	pt = Table(table_frame)
	data_frame = get_tags(user, password)
	pt.model.df = data_frame
	pt.show()

	pt.unbind_all("<Tab>")
	pt.unbind_all("<Return>")


	# main loop
	view_root.mainloop()




#**********************************************************************************************
#						  		      END VIEW SCREEN
#**********************************************************************************************