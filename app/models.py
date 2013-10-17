import datetime

class storedPassword():

	def __init__(self, owner, username, password):
		self.owner = owner
		self.username = username
		self.password = password

	def getPassword(self):
		return self.password

	def asDict(self):
		mdict = {'owner': self.owner,
				'username': self.username,
				'password': self.password}

		return mdict