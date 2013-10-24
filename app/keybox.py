import configparser
import logging

from flask import Flask, session
from flaskext.xmlrpc import XMLRPCHandler, Fault

from flask import render_template

from pymongo import MongoClient

import tools
from models import *

config = configparser.ConfigParser()
config.read('config.ini')

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
handler = XMLRPCHandler('api')
handler.connect(app, '/api')

client = MongoClient(tools.composeDB(config['Database']))
db = client[config['Database']['DB_NAME']]

"""
USERS
"""

@handler.register
def login(username, password):
    logger.info('Login attempt by %s', username)
    res = User.login(db, username, password)
    if not res:
        logger.debug('Login failed for %s', username)
        return False
    else:
        logger.debug('Login success for %s', username)
        session['username'] = username        
        return User.simplify(res)

@handler.register
def welcome(username='nobody'):
    logger.info('Server test by %s', username)
    res = "Welcome %s! Server is online!" % username
    return res

""" 
USERS

"""

@handler.register
def createUser(username, password, email):
    logger.debug('Creating %s as user', username)
    data = {
        'username': username,
        'password': password,
        'email': email
    }

    try:
        res = User.create(db, data)
        logger.debug('User %s created', username)
    except Exception:
        logger.debug('User %s creation failed', username)
        return False
    return True

"""
CREDENTIALS
"""

@handler.register
def saveCredential(data):

    logger.debug('Creating new credential')
    try:
        res = Credential.create(db, data)
        logger.debug('New credential created')
    except Exception:
        logger.debug('New credential creation failed')
        return False
    return True
	
@handler.register
def getPassword(title, owner):
    logger.info('Getting password for %s', owner)
    creds = Credential.lookup(db, title, owner)

    res = []

    if not creds:
        logger.debug('No credential with title %s found', title)
        return False
    else:
        logger.debug('Credential found for %s', owner)
        for c in creds:            
            res.extend([Credential.simplify(c)])

        return res

@handler.register
def updatePassword(title, owner, data):
    logger.info('Updatting password for %s', owner)

    creds = Credential.lookup(db, title, owner)

    # FIXME: this cycle must look better!
    if creds:
        for c in creds:
            for k in data.keys():
                if data[k] == '' or data[k] == False: 
                    data[k] = c[k]        
            
            data['_id'] = c['_id']

        creds = Credential.update(db, data)
        
        if not creds:
            logger.debug("Problem during credential with title %s update" % title)
            return False
        else:
            logger.debug("Successfully updated credential with title %s" % title)
            return True
    else:
        logger.debug("No credential with title %s found during update" % title)
        return False

@app.route('/hello/')
def hello():
    return render_template('index.html')

if __name__ == '__main__':    
    app.secret_key = '0m1@b3l@.m@dun1n@.ch3.t3.br1l1.d@#lunt@n'
    app.run()

