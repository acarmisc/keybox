import configparser
from pymongo import MongoClient
from models import *

import tools

config = configparser.ConfigParser()
config.read('config-test.ini')

print "Inizializing new database named *%s* base on config" % config['Database']['DB_NAME']
# TODO: add some checks before continue and for the operations

client = MongoClient("mongodb://%s:%s/%s" % 
		(config['Database']['DB_HOST'], 
		config['Database']['DB_PORT'], 
		config['Database']['DB_NAME']))

db = client[config['Database']['DB_NAME']]

print "Successfully initialized DB"

db.add_user(config['Database']['DB_USER'], config['Database']['DB_PASS'])

print "Successfully added administrator"

print "Testing the connection"

client = MongoClient(tools.composeDB(config['Database']))
db = client[config['Database']['DB_NAME']]

print "FIRST USER INFORMATIONS:"
username = raw_input('username: ')
password = raw_input('password: ')
email = raw_input('e-mail: ')

data = {
    'username': username,
    'password': password,
    'email': email
}

res = User.create(db, data)    

print "Setup completed"