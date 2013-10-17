from flask import Flask
from flaskext.xmlrpc import XMLRPCHandler, Fault
from pymongo import MongoClient

from models import *

app = Flask(__name__)

handler = XMLRPCHandler('api')
handler.connect(app, '/api')

#----------------------------------------
# database
#----------------------------------------

DB_NAME = 'keybox'

client = MongoClient()
client = MongoClient('mongodb://admin:admin@localhost:27017/')
db = client[DB_NAME]

@handler.register
def welcome(username=False):
	if not username:
		raise Fault("unknown_user", "I don't know you!")

	users = db.users
	found = users.find_one({'name': username})
	if found:
		return "E-mail: %s" % found['email']
	else: 
		return "No results found."

@handler.register
def savePassword(owner, username, password):
	new = storedPassword(owner, username, password).asDict()
	pwd = db.storedPassword	
	
	try:
		stored_id = pwd.insert(new)
		return "Saved."
	except ValueError:	
		return "Error saving."

app.run()