import configparser
import logging

from flask import Flask
from flaskext.xmlrpc import XMLRPCHandler, Fault
from pymongo import MongoClient

import tools

from models import *

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
handler = XMLRPCHandler('api')
handler.connect(app, '/api')

config = configparser.ConfigParser()
config.read('config.ini')

client = MongoClient()

try:
    client = MongoClient(tools.composeDB(config['Database']))
except:
    logger.error('Error connecting to DB: %s' % tools.composeDB(config['Database']))

db = client[config['Database']['DB_NAME']]

@handler.register
def welcome(username=False):
    logger.debug("Welcome called")

    if not username:
        raise Fault("unknown_user", "I don't know you!")

	users = db.users
	found = users.find_one({'name': username})
	if found:
		return "E-mail: %s" % found['email']
	else: 
		return "No results found."

@handler.register
def createUser(username, password, email):
    new = User(username, password, email).asDict()
    u = db.User

    if not u.find_one({'username': username}):
        try:
            uid = u.insert(new)
        except ValueError:
            return "Error saving."
    else:
        return "Username exists."

@handler.register
def savePassword(owner, key, username, password):
	new = storedPassword(owner, key, username, password).asDict()
	pwd = db.storedPassword	
	
	try:
		stored_id = pwd.insert(new)
		return "Saved."
	except ValueError:	
		return "Error saving."

@handler.register
def getPassword(key, owner):
    logger.debug("%s ask for a password" % owner)

    res = []
    
    pwds = db.storedPassword
    items = pwds.find({'key': key,'owner': owner})
    for i in items:
        print i
        res.extend([{'username': i['username'], 
                    'password': i['password']}])
    
    print res
    return res

if __name__ == '__main__':
    app.run()