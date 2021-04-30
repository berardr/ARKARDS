#*************************************************************************************
# The purpose of this file is recieve requests from the hololense and then gather
# information from the db to send back to the hololens
#*************************************************************************************

import paho.mqtt.client as mqtt
import time
import sys
import json
import base64
from database import *

#broker to connect the client to
BROKER = "test.mosquitto.org"

# lists for holding the anchors and tags
ANCHOR_LIST = []

# function for disconnect callback
def on_disconnect(client, userdata, rc):
    # print disconnect message
    print("Client is disconnected with RC: ", rc)
    # if disconnected then clear the list since it probably means we will get new anchors on the turn on
    ANCHOR_LIST.clear()

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


# function for sending the anchors
def send_anchors(client):

    # loop through the anchor list and send over the anchors
    for anchor in ANCHOR_LIST:
        id = anchor["configuration"]["label"]
        pub_topic = "dwm/node/anchors/" + id
        anchorJson =  json.dumps(anchor)
        client.publish(pub_topic, anchorJson)
        print("Anchor Sent")

# function for sending the tags
def send_tag(client):

    # loop through the tag list and send over the tags
    for tag in TAG_LIST:
        id = tag["configuration"]["label"]
        pub_topic = "dwm/node/anchors/" + id
        tagJson =  json.dumps(anchor)
        client.publish(pub_topic, tagJson)
        print("Tag Sent")

# function for the anchor request call back
def request_anchors_callback(client, userdata, msg):
    send_anchors(client)

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
def config_callback(client, userdata, msg):

    # try and except, this is the lazy of handling if a message is not a config
    try:
        # message decdoing
        msg_decode = str(msg.payload.decode("utf-8","ignore"))
        msg_list = json.loads(msg_decode)

        # get the anchor config information
        nodeType = msg_list["configuration"]["nodeType"]
        # get the id and position
        id = msg_list["configuration"]["label"]
        postion = msg_list["configuration"]["anchor"]["position"]

        # make sure the config message is from an anchor if so add it to the list
        if (nodeType == "ANCHOR"):

            # print recieve message
            print("Anchor Config Message Recieved")

            not_found_anchor = True # bool for checking the loop

            # if the list is empty add the message
            if not ANCHOR_LIST:
                ANCHOR_LIST.append(msg_list)
                print("Anchor Added To List")

                # loop through the current list and makes sure the anchor is not added already
                # if it is not added then add it otherwise if its there and the positon is different update it
                # finally added otherwise
            else:
                for anchor in ANCHOR_LIST:
                    if anchor["configuration"]["label"] == id: # here we check to see if the anchor is in the list
                        if anchor["configuration"]["anchor"]["position"] != postion: # check if the position has chenged
                            anchor["configuration"]["anchor"]["position"] = postion # update postion if it has
                            print("Anchor Updated") # print message
                            not_found_anchor = False
                            break # break from the loop we are done
                        else:
                            print("Anchor Already Added") # anchor is in the list with no changes so dont duplicate the list
                            not_found_anchor = False
                            break # break we are done

                if not_found_anchor:
                    ANCHOR_LIST.append(msg_list) # we loop through and didnt find it so add it
                    print("Anchor Added To List") # print message
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
    client = mqtt.Client()

    # set the callback fucntions for connection and log
    client.on_connect = on_connect
    #client.on_log = on_log # uncomment to see log, leave comment to suppress log
    client.on_disconnect = on_disconnect

    # set the callback functions for the topics
    client.message_callback_add("dwm/holo/login", login_callback)
    client.message_callback_add("dwm/holo/requesttaginfo", tag_callback)
    client.message_callback_add("dwm/holo/requestanchors", request_anchors_callback)

    # this call back is for the messages for the config messages
    client.message_callback_add("dwm/node/+/uplink/config", config_callback)

    # connect tothe broker
    print("Connecting to broker: " + BROKER)
    client.connect(BROKER, keepalive = 5)

    # subscribe to the login, tags, and anchor requests
    client.subscribe("dwm/holo/login", qos = 1)
    client.subscribe("dwm/holo/requesttaginfo", qos = 1)
    client.subscribe("dwm/holo/requestanchors", qos = 1)

    # here we will sub to listen for config messages from the anchors
    client.subscribe("dwm/node/+/uplink/config", qos = 1)

    # start the loop for call backs to be processed
    client.loop_forever()

# try and start the stript, error if not
try:
    start_mqtt()

except e:
    print(e)
