import sys

from clientTools import colorize
import xmlrpclib

server = xmlrpclib.ServerProxy('http://localhost:5000/api')

current = {}

while not current:

	# testing arguments
	if len(sys.argv) > 1:
		test_user = sys.argv[1]
		test_pass = sys.argv[2]
	else:
		test_user = raw_input("Login as: ")
		test_pass = raw_input("Password: ")

	res = server.login(test_user, test_pass)
	if res:
		current = res

while True:
	print colorize("--- MENU ---", 'blue')
	print "[%s] create user" % colorize("1", 'blue')
	print "[%s] save new credential" % colorize("2", 'blue')
	print "[%s] get password" % colorize("3", 'blue')
	print "[%s] debug dump" % colorize("8", 'blue')
	print "[%s] test server" % colorize("9", 'blue')
	print "[%s] initialize DB" % colorize("0", 'blue')
	choose = raw_input("Select an option: ")

	if choose == '0':
		name = raw_input("New DB name: ")
		print "TODO"

	elif choose == '8':
		print current

	elif choose == '9':
		username = raw_input("Insert your username: ")
		print server.welcome(username)
	
	elif choose == '1':
		username = raw_input("Insert new username: ")
		password = raw_input("Insert password: ")
		email = raw_input("Insert e-mail: ")

		res = server.createUser(username, password, email)
		
		if not res:
			print "Unable to create new user"			
		else:
			print "User created"
		
	elif choose == '2':
		print "creating..."
		owner = current['username']
		title = raw_input("Select a name for this item: ")
		username = raw_input("Insert the username: ")
		password = raw_input("Insert the password: ")
		url = raw_input("URL for those credential: ")
		note = raw_input("Notes: ")

		data = {
			'owner': owner,
			'title': title,
			'username': username,
			'password': password,
			'url': url,
			'note': note
		}

		res = server.saveCredential(data)

		if not res:
			print "Unable to create new credential"
		else:
			print colorize("Credential created",'green')

	elif choose == '3':
        #TODO: return keys and not values!!!
		owner = current['username']
		title = raw_input("Item title: ")

		res = server.getPassword(title, owner)
		print res
