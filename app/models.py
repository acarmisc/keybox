import hashlib
m = hashlib.md5()

class Env():
    def initDb():
        #TODO: create database with base data
        pass

class Credential():
    def __init__(self):
        self.title = ''
        self.username = ''
        self.password = ''
        self.url = ''
        self.note = ''
        self.owner = ''

    @staticmethod
    def asDict(self):
        mdict = {
                'title': self.title,
                'username': self.username,
                'password': self.password,
                'url': self.url,
                'note': self.note,
                'owner': self.owner
        }

        return mdict

    @staticmethod
    def simplify(credential):
        mdict = {
                'title' : credential['title'],
                'username' : credential['username'],
                'password' : credential['password'],
                'url': credential['url'],
                'note': credential['note'],                
                }
        return mdict

    @staticmethod
    def create(db, data):
        collection = db.Credential
        
        res = collection.insert(data)
        return res

    @staticmethod
    def update(db, data):
        collection = db.Credential    
        
        if collection.update({'_id': data['_id']}, data):
            return True
        else:
            return False

    @staticmethod
    def lookup(db, title, owner):
        collection = db.Credential
        if not title:
            params = {'owner': owner}
        else:
            params = {'title': title, 'owner': owner}
        res = collection.find(params)
        return res

class User():
    def __init__(self):
        self.username = ''
        self.password = ''
        self.email = ''

    @staticmethod
    def asDict(self):
        mdict = {
                'username': self.username,
                'password': self.password,
                'email': self.email
                }

        return mdict

    @staticmethod
    def simplify(user):
        mdict = {
                'username' : user['username'],
                'password' : user['password'],
                'email' : user['password']
                }
        return mdict

    @staticmethod
    def login(db, username, password):
        collection = db.User
        password = m.update(password)
        password = m.hexdigest()
        res = collection.find_one({'username': username, 'password': password})
        return res

    @staticmethod
    def create(db, data):
        collection = db.User
        data['password'] = m.update(data['password'])
        data['password'] = m.hexdigest()
        found = collection.find_one({'username': data['username'], 'password': data['password']})
        if found:
            return False
        else:
            res = collection.insert(data)
        return res
