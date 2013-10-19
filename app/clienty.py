import xmlrpclib
server = xmlrpclib.ServerProxy('http://localhost:5000/api')

current = {}
current['username'] = raw_input("Login as: ")
current['password'] = raw_input("Password: ")

while True:
	print "--- MENU ---"
	print "[1] create user"
	print "[2] save password"
	print "[3] get password"
	print "[0] test server"
	choose = input("Select an option: ")

	if choose == 0:
		username = raw_input("Insert your username: ")
		print server.welcome(username)
	elif choose == 1:
		username = raw_input("Insert new username: ")
		password = raw_input("Insert password: ")
		email = raw_input("Insert e-mail: ")

		print server.createUser(username, password, email)

	elif choose == 2:
		owner = current['username']
		key = raw_input("Select a name for this item: ")
		username = raw_input("Insert new username: ")
		password = raw_input("Insert password: ")		
		
		print server.savePassword(owner, key, username, password)

	elif choose == 3:
		owner = current['username']
		key = raw_input("Item name: ")

		res = server.getPassword(key, owner)
		print res
