# *************************************************************************************************
#										DATBASE FILE
# The purpose of this file is to set up all the functions that will interact with the database
# Each screen will be able to access this file and call the desired function
#**************************************************************************************************

# import modules
import mysql.connector
import os
from datetime import datetime
import subprocess
import pandas as pd


# variables for connections, host is local in this case since on this machine,
HOST_ID = "localhost"

# this function creates the schema, also creates tables to go into schema
def start_db(user_id, password_id):
	try:
		# connect to mysql sever
		mydb = mysql.connector.connect(
			host = HOST_ID,
			user = user_id,
			password = password_id
		)

		# cursor instance
		cursor = mydb.cursor()

		# create arkards database if not already
		cursor.execute("CREATE DATABASE IF NOT EXISTS arkards")

		# create table if not already
		cursor.execute("CREATE TABLE IF NOT EXISTS arkards.tags (tag VARCHAR(100) NOT NULL PRIMARY KEY, first_name VARCHAR(25), last_name VARCHAR(25), height VARCHAR(25), weight VARCHAR(25), sex VARCHAR(25), pic VARCHAR(10000))")

		# commit close connections
		mydb.commit()
		mydb.close()

		return True

	except mysql.connector.Error as err:
		return False

# this function is for adding a tag to the db
def add_tag(user_id, password_id, tag, first_name, last_name, height, weight, sex, pic):

		try:
			# connect to mysql sever
			mydb = mysql.connector.connect(
				host = HOST_ID,
				user = user_id,
				password = password_id
			)

			# cursor instance
			cursor = mydb.cursor()

			# SQL query
			query = "INSERT INTO arkards.tags (tag, first_name, last_name, height, weight, sex, pic) VALUES(%s, %s, %s, %s, %s, %s, %s)"

			# data tuple for values
			values = (tag, first_name, last_name, height, weight, sex, pic)

			# execute the command
			cursor.execute(query, values)

			# commit close connections
			mydb.commit()
			mydb.close()

			return True

		except mysql.connector.Error as err:

			print(err)
			return False



# this function is for clearing all the tags from the DB

def clear_tags(user_id, password_id):

	try:
		# connect to mysql sever
		mydb = mysql.connector.connect(
		host = HOST_ID,
		user = user_id,
		password = password_id
		)

		# cursor instance
		cursor = mydb.cursor()

		# SQL query
		query = "DELETE FROM arkards.tags"

		# execute the command
		cursor.execute(query)

		# commit close connections
		mydb.commit()
		mydb.close()

		return True

	except mysql.connector.Error as err:

		print(err)
		return False


# this function is for creating MySQL dump file to backup directory with timestamp

def backup_db(user_id, password_id):

	# variables for the time
	time_now = datetime.now()
	time_now_string = time_now.strftime("%m_%d_%Y - %H_%M_%S")

	# check directory for backup
	if not os.path.exists("Backup"):
	    os.makedirs("Backup")

	# create file name
	file_name = "Backup/" + time_now_string + ".sql"


	# easiest way, is call call through cmd, shows warning about password, this can be ignored since it thinks the password is being entered.
	with open(file_name, "w") as output:
		c = subprocess.Popen(['C:/Program Files/MySQL/MySQL Server 8.0/bin/mysqldump', '-u',user_id,'-p%s'%password_id, 'arkards'], stdout= output, shell=True)


# function to add new user, first we must create then grant privelages
def add_user(user_id, password_id, new_user, new_password):

	user_check = create_user(user_id, password_id, new_user, new_password)

	if user_check:

		priv_check = new_user_priv(user_id, password_id, new_user, new_password)

		if priv_check:

			return True

		else:

			return False
	else:

		return False

# function for creating user, returns true if succesful
def create_user(user_id, password_id, new_user, new_password):

	try:
		# connect to mysql sever
		mydb = mysql.connector.connect(
		host = HOST_ID,
		user = user_id,
		password = password_id
		)

		# cursor instance
		cursor = mydb.cursor()

		# SQL query
		query = "CREATE USER %s@%s IDENTIFIED BY %s"

		#data tuple
		data = (new_user, HOST_ID, new_password)

		# execute the command
		cursor.execute(query, data)

		# commit close connections
		mydb.commit()
		mydb.close()

		return True

	except mysql.connector.Error as err:
		print(err)
		return False

# function for granting privelgage, returns ture if succesful
def new_user_priv(user_id, password_id, new_user, new_password):


	try:
		# connect to mysql sever
		mydb = mysql.connector.connect(
		host = HOST_ID,
		user = user_id,
		password = password_id
		)

		# cursor instance
		cursor = mydb.cursor()

		# SQL query
		query = "GRANT ALL PRIVILEGES ON *.* TO %s@%s"

		#data tuple
		data = (new_user, HOST_ID)

		# execute the command
		cursor.execute(query, data)

		# commit close connections
		mydb.commit()
		mydb.close()

		return True

	except mysql.connector.Error as err:

		print(err)
		return False


# function for getting the users
def get_users(user_id, password_id):

		# connect to mysql sever
		mydb = mysql.connector.connect(
		host = HOST_ID,
		user = user_id,
		password = password_id
		)

		# cursor instance
		cursor = mydb.cursor()

		# SQL query
		query = "SELECT user from mysql.user WHERE user NOT LIKE 'mysql%'"
		df = pd.read_sql(query, mydb)

		# execute the command
		cursor.execute(query)

		# fetch all the user records
		sql_users = cursor.fetchall()

		final = pd.DataFrame(sql_users, columns = df.columns)

		# commit close connections
		mydb.commit()
		mydb.close()

		return final

# function for dropping a user
def drop_user(user_id, password_id, user_drop):

	try:
		# connect to mysql sever
		mydb = mysql.connector.connect(
		host = HOST_ID,
		user = user_id,
		password = password_id
		)

		# cursor instance
		cursor = mydb.cursor()

		# SQL query
		query = "DROP USER %s@%s"

		#data tuple
		data = (user_drop, HOST_ID)

		# execute the command
		cursor.execute(query, data)

		# commit close connections
		mydb.commit()
		mydb.close()

		return True

	except mysql.connector.Error as err:

		print(err)
		return False

# function for getting the tag
def get_tags(user_id, password_id):

		# connect to mysql sever
		mydb = mysql.connector.connect(
		host = HOST_ID,
		user = user_id,
		password = password_id
		)

		# cursor instance
		cursor = mydb.cursor()

		# SQL query
		query = "SELECT * from arkards.tags"
		df = pd.read_sql(query, mydb)

		# execute the command
		cursor.execute(query)

		# fetch all the user records
		tags = cursor.fetchall()

		final = pd.DataFrame(tags, columns = df.columns)

		# commit close connections
		mydb.commit()
		mydb.close()

		return final

# function for dropping a user
def drop_tag(user_id, password_id, tag_drop):

	try:
		# connect to mysql sever
		mydb = mysql.connector.connect(
		host = HOST_ID,
		user = user_id,
		password = password_id
		)

		# cursor instance
		cursor = mydb.cursor()

		# SQL query
		query = "DELETE FROM arkards.tags WHERE tag = %s"

		#data tuple
		data = (tag_drop,)

		# execute the command
		cursor.execute(query, data)

		# commit close connections
		mydb.commit()
		mydb.close()

		return True

	except mysql.connector.Error as err:

		print(err)
		return False

# function for checking a tag
def check_tag(user_id, password_id, tag_check):

	try:
		# connect to mysql sever
		mydb = mysql.connector.connect(
			host = HOST_ID,
			user = user_id,
			password = password_id
		)

		# cursor instance
		cursor = mydb.cursor()

		# SQL query
		query = "SELECT * FROM arkards.tags WHERE tag = %s"

		#data tuple
		data = (tag_check,)

		# execute the command
		cursor.execute(query, data)

		# fetch the tag record
		tag = cursor.fetchall()

		# commit close connections
		mydb.commit()
		mydb.close()

		# if there is no tag aka empty list then return false otherwise the tag is there
		if not tag:
			return False
		else:
			return True

	except mysql.connector.Error as err:

		print(err)
		return False

# function for getting tag info
def get_tag_info(user_id, password_id, tag_get):

	try:
		# connect to mysql sever
		mydb = mysql.connector.connect(
		host = HOST_ID,
		user = user_id,
		password = password_id
		)

		# cursor instance
		cursor = mydb.cursor()

		# SQL query
		query = "SELECT * FROM arkards.tags WHERE tag = %s"

		#data tuple
		data = (tag_get,)

		# execute the command
		cursor.execute(query, data)

		# fetch the tag record
		tag = cursor.fetchall()

		# commit close connections
		mydb.commit()
		mydb.close()

		return tag

	except mysql.connector.Error as err:
		pass



# *************************************************************************************************
#										END DATBASE FILE
#**************************************************************************************************
