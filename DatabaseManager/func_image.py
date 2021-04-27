# *************************************************************************************************
#										FUNC IMAGE
# The purpose of this file is to take the given image by the user, resize it and copy it to a known
# directory. The will name the file based on the tag assigned to it, and will save the path on to
# the DB. This is the peferred method to saving images (vs BLOB) to a DB since there are many 
# downsides to saving them directly in the table
#**************************************************************************************************

import os
from PIL import Image, ImageTk

MAX_SIZE = 512

def image_open(path, tag):

	# open the image
	pic = Image.open(path)

	# get size of the image and make with the largest MAX_SIZE width or height
	size = pic.size
	ratio = min(MAX_SIZE/size[0], MAX_SIZE/size[1])
	new_width = int(size[0]*ratio)
	new_height = int(size[1]*ratio)

	# resize the image
	resize = pic.resize((new_width, new_height), Image.ANTIALIAS)

	# make directory for storing new images 
	if not os.path.exists("Tag Images"):
		os.makedirs("Tag Images")

	# new file name is that tag id an convert to png
	new_file_name = "Tag Images/" + str(tag) + ".png"

	# save the new image to the directory
	resize.save(new_file_name)
	
	# return the new file path name so we can save it to the DB
	return new_file_name

# function for clearing all the images
def image_clear():

	try:
		for file in os.scandir("Tag Images/"):
			os.remove(file.path)

	except:
		pass


# function for viewing the picture
def image_view(path):

	return ImageTk.PhotoImage(Image.open(path))

#******************************************************************************************************
#										END FUNC IMAGE
#******************************************************************************************************

