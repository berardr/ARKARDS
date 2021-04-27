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

# fucntion for on_log callback
def on_log(clinet, userdata, level, buf):
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

    print(msg_list)

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

    print(info)

# fuction for the tag_callback
def tag_callback(client, user, msg):
    # message decdoing
    msg_decode = str(msg.payload.decode("utf-8","ignore"))
    msg_list = json.loads(msg_decode)

    print(msg_list)

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
    #broker to connect to
    broker = "192.168.1.35"
    client = mqtt.Client()

    # set the callback fucntions for connection and log
    client.on_connect = on_connect
    #client.on_log = on_log # uncomment to see log, leave comment to suppress log

    # set the callback functions for the topics
    client.message_callback_add("dwm/holo/login", login_callback)
    client.message_callback_add("dwm/holo/requesttaginfo", tag_callback)

    # connect tothe broker
    print("Connecting to broker: " + broker)
    client.connect(broker)

    # subscribe to the login and tags
    client.subscribe("dwm/holo/login")
    client.subscribe("dwm/holo/requesttaginfo")

    # start the loop for call backs to be processed
    client.loop_start()

    # wait 1 second
    time.sleep(1)

    # print the heading and the options
    print("************************************************")
    print("*       LISTENING FOR LOGIN AND TAGS          *")
    print("************************************************")
