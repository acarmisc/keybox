import sys
from clientTools import colorize
import xmlrpclib
import configparser


config = configparser.ConfigParser()
config.read('config.ini')

server = xmlrpclib.ServerProxy("http://%s:%s/api" % (config['SERVER']['host'], config['SERVER']['port']))

current = {}

while True:

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

	print ""
	print ""
	print colorize("--- MENU ---", 'blue')
	print "[%s] list credential" % colorize("1", 'blue')
	print "[%s] save new credential" % colorize("2", 'blue')
	print "[%s] get password" % colorize("3", 'blue')
	print "[%s] update password" % colorize("4", 'blue')
	print "[%s] create user" % colorize("7", 'blue')
	print "[%s] debug dump" % colorize("8", 'blue')
	print "[%s] test server" % colorize("9", 'blue')
	print "[%s] Logout" % colorize("0", 'blue')
	choose = raw_input("Select an option: ")

	if choose == '0':
		current = False

	elif choose == '1':
		owner = current['username']
		print "All stored credential for %s" % owner

		res = server.getPassword(False, owner)

		print " TITLE"
		print "======================="
		for r in res:
			print "%s (%s)" % (r['title'], r['username'])


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
		owner = current['username']
		title = raw_input("Item title: ")
		tmpl = "URL: %s \nUsername: %s \nPassword: %s \nNotes: %s"
		results = server.getPassword(title, owner)
		if results:
			for res in results:
				values = (colorize(res['url'],'green'),
							colorize(res['username'],'green'),
							colorize(res['password'],'green'),
							colorize(res['note'],'green'))

				res = tmpl % values
				print res
		else:
			print colorize("No results found.", "fail")

	elif choose == '4':
		data = {}
		results = ''
		owner = current['username']
		data['owner'] = owner
		while not results:
			title = raw_input("Credential to update: ")
			results = server.getPassword(title, owner)
			if not results:
				print "No credential found. Retry."

		# new datas
		data['title']= raw_input("Update the title or press ENTER: ")
		data['username']= raw_input("Update the username or press ENTER: ")
		data['password']= raw_input("Update the password or press ENTER: ")
		data['url']= raw_input("Update the URL or press ENTER: ")
		data['note']= raw_input("Update the notes or press ENTER: ")

		result = server.updatePassword(title, owner, data)
		print result

	elif choose == '7':
		username = raw_input("Insert new username: ")
		password = raw_input("Insert password: ")
		email = raw_input("Insert e-mail: ")

		res = server.createUser(username, password, email)

		if not res:
			print "Unable to create new user"
		else:
			print "User created"

	elif choose == '8':
		print current

	elif choose == '9':
		username = raw_input("Insert your username: ")
		print server.welcome(username)

