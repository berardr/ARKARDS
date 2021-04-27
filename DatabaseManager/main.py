# this is the main file that will start the application

from login import *
from database import start_db
from menu import start_menu
from mqtt_db import start_mqtt

# launch MQTT, if not write error
try:
    start_mqtt()
except:
    print("Problem Starting MQTT. Please Check Connection")

print("Starting GUI...")
start_login()
