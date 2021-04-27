#*************************************************************************************
# The purpose of this file is recieve requests from the hololense and then gather
# information from the db to send back to the hololense
#*************************************************************************************

import paho.mqtt.client as mqtt
import time
import sys
import json
import base64
from database import *

#broker to connect the client to
BROKER = "192.168.1.35"

# list for holding the anchors, and counter to count how many we have
ANCHOR_LIST = []

# function for disconnect callback
def on_disconnect(client, userdata, rc):
    # print disconnect message
    print("Client is disconnected with RC: ", rc)

# fucntion for on_log callback
def on_log(client, userdata, level, buf):
    print("log: "+ buf)

# function for on connect callback
def on_connect(client, userdata, level, rc):
    # if connection is good then print OK otherwise report the return code
    if rc == 0:
        print("Connected OK")
    else:
        print("Bad Connection, ERROR = ", rc)

# function for the on_message callback
def login_callback(client, userdata, msg):

    # message decdoing then convert from JSON to list
    msg_decode = str(msg.payload.decode("utf-8","ignore"))
    msg_list = json.loads(msg_decode)

    # get the user name and password then save it
    user_id = msg_list["user_id"]
    password_id = msg_list["password_id"]

    # call the startdb function, this fuction also check if we can login, if so then
    # return true otherwise false, then i guess publish it back to another topic where
    # the holo will bhe listening
    check = start_db(user_id, password_id)

    # prep the message back with the username and valid or not
    info = {
                "user_id": user_id,
                "valid" : check
                }

    infoJson = json.dumps(info)

    # plublish back to to the results where the holo will listen
    client.publish("dwm/node/loginresults", infoJson)
    print("Login Response Published")

    # only send the anchors if the login is valid
    if check:
        for anchors in ANCHOR_LIST:
            time.sleep(0.5) #sleep a little between messages
            anchorJson =  json.dumps(anchors)
            client.publish("dwm/node/anchors")
            print("Anchor Config Published")


# fuction for the tag_callback
def tag_callback(client, userdata, msg):
    # message decdoing
    msg_decode = str(msg.payload.decode("utf-8","ignore"))
    msg_list = json.loads(msg_decode)

    # get the tag number
    tag = msg_list["tag_id"]
    user_id = msg_list["user_id"]
    password_id = msg_list["password_id"]

    # check to moke sure it is in the DB, use login info
    check = check_tag(user_id, password_id, tag)

    # if we find the tag, take the info and populated the message. otherwise invalid
    if check:
        tag_info = get_tag_info(user_id, password_id, tag) # changed the user and password to be from the tag message, hard code is for testing.

        # convert the image to a basd64 string
        image_string = image_to_base64(tag_info[0][6])

        # tag message to be sent
        tag_message = {
                        "tag" : tag_info[0][0],
                        "first_name" : tag_info[0][1],
                        "last_name" : tag_info[0][2],
                        "height" : tag_info[0][3],
                        "weight" : tag_info[0][4],
                        "sex" : tag_info[0][5],
                        "pic" : image_string
                        }

    else:
        # tag invalid message
        tag_message = {
                        "tag" : tag,
                        "first_name" : "INVALID",
                        "last_name" :"INVALID",
                        "height" :"INVALID",
                        "weight" : "INVALID",
                        "sex" : "INVALID",
                        "pic" : "INVALID"
                        }
    # convert to json
    tag_json = json.dumps(tag_message)

    # publish to mqtt broker
    client.publish("dwm/node/tag",tag_json)
    print("Tag Info Published")

# function for getting anchor configs then prepping them to send to the holo
def anchor_callback(client, userdata, msg):

    # try and except, this is the lazy of handling if a message is not a config
    try:
        # message decdoing
        msg_decode = str(msg.payload.decode("utf-8","ignore"))
        msg_list = json.loads(msg_decode)

        # get the anchor config information
        nodeType = msg_list["configuration"]["nodeType"]

        # make sure the config message is from an anchor if so add it to the list
        if (nodeType == "ANCHOR"):
            # add the messgae from the DWM to the list
            ANCHOR_LIST.append(msg_list)
    except:
        pass

# function for turning an image into base64
def image_to_base64(path):
    # take the path and open the file
    with open(path, "rb") as img_file:
        # encode with base 64
        b64_string = base64.b64encode(img_file.read())

    # this is suppose to remove the leading "b'"
    decoded_b64_string = b64_string.decode("utf-8")

    # return the string
    return decoded_b64_string

# fuction for starting the connection and prompting user options
def start_mqtt():
    #client
    client = mqtt.Client("ARK_DB", clean_session = False)

    # set the callback fucntions for connection and log
    client.on_connect = on_connect
    #client.on_log = on_log # uncomment to see log, leave comment to suppress log
    client.on_disconnect = on_disconnect

    # set the callback functions for the topics
    client.message_callback_add("dwm/holo/login", login_callback)
    client.message_callback_add("dwm/holo/requesttaginfo", tag_callback)

    # this call back is for the messages for the anchors
    client.message_callback_add("dwm/node/#", anchor_callback)

    # connect tothe broker
    print("Connecting to broker: " + BROKER)
    client.connect(BROKER, keepalive = 5)

    # subscribe to the login and tags
    client.subscribe("dwm/holo/login", qos = 1)
    client.subscribe("dwm/holo/requesttaginfo", qos = 1)

    # here we will sub to listen for config messages from the anchors
    client.subscribe("dwm/node/#", qos = 1)

    # start the loop for call backs to be processed
    client.loop_start()

    # wait 1 second
    time.sleep(1)

    # print the heading and the options
    print("************************************************")
    print("*       LISTENING FOR LOGIN AND TAGS          *")
    print("************************************************")
