# This file handles adding and removing objects from the json file
# In the future this will be replaced by a database

#import libraries
import json


#function for adding
def add():

    print("\n******ADD MENU******\n") #print heading
    id = input("Enter ID: ") #this will be used as the ID for the JSON

    check = True #this will check for correct user input

    #will loop until either A or T are given for the node type
    while(check):
        type = input("Enter type \"A\" for anchor or \"T\" for tag: ")
        if type != "A" and type != "T":
            print("INVALID ENTRY TRY AGAIN!\n") #print error message
        else:
            check = False #correct input is given, break loop by setting to false

    #if node is an anchor then it will require location cooridnates and quality
    if type == "A":
        x = input("Enter X location: ")
        y = input("Enter Y location: ")
        z = input("Enter Z location: ")
        quality = "100"

    #if node is a tage then location and quality are set to blank since they will be recieved
    if type == "T":
        x = {}
        y = {}
        z = {}
        quality = {}

    #create dictionary with the required information
    node_dict = {id:{'label':'DW' + id.upper(),
            'config': {},
            'status': {},
            'type': type,
            'loc': {
            'x': x,
            'y': y,
            'z': z,
            'qual': quality
            }}}

    #file path to json file, this is in the same directory so a full path is not needed.
    json_file_path = ("node_ref.json")

    file = open(json_file_path,"r+") #open json file with read and write

    json_string = json.loads(file.read()) # reads file from the top and converts to json string
    json_string.update(node_dict) # this joins the unser json entry to the string
    node_json = json.dumps(json_string, indent = 2) #create json node from the dictionary

    file.seek(0) #return the file cusor to the top of the file
    file.truncate() #now truncate the file removing everything
    file.write(node_json)#now write the new json object with the existing information plus what the user entered
    file.close()#close the file

    #print that it is beeing added
    print("ADDING...\n")



#fuction for removing
def remove():

    print("\n******REMOVE MENU******\n") #print heading
    id = input("Enter ID to remove: ") #this will be used as the ID to remove

    #file path to json file, this is in the same directory so a full path is not needed.
    json_file_path = ("node_ref.json")

    file = open(json_file_path,"r+") #open json file with read and write
    data = json.loads(file.read()) # reads file from the top and converts to dictionary

    found = False #flag for checking if the item is in the dictionary

    #loop through the dictionarry to see if the id is in it
    for element in data:
        if id in element:
            found = True

    # if the id is not found print and go back to main screen, if found pop it and update the file
    if (not found):
        print("NO SUCH ID EXISTS\n")
    else:
        data.pop(id) #remove the entry from the dictionary
        data = json.dumps(data, indent = 2) #create json object from dictionary with the removed node
        file.seek(0) #return the file cusor to the top of the file
        file.truncate() #now truncate the file removing everything
        file.write(data)#now write the new json object
        file.close()#close the file
        print("REMOVING...\n")

#function for initatlizing adding or removing node
def start():
    #loop until user wants to exit
    while (1):
        print("Welecome to JSON editing!\nPlease select mode: \n\t1) add node \n\t2) remove node \n\t3) exit") #print start message
        mode = input("\nINPUT: ")

        if mode == "1":
            add()
        elif mode == "2":
            remove()
        elif mode == "3":
            print("EXITING EDIT MODE...")
            return
        else:
            print("INVALID MODE PLEASE TRY AGAIN!\n")
