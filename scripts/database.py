import random
import string
import hashlib

from google.appengine.ext import db

class User(db.Model):
	fname = db.StringProperty(required = True)
	lname = db.StringProperty(required = True)
	email = db.StringProperty(required = True)
	email_pw_salt = db.StringProperty(required = True)

	@staticmethod
	def make_salt():
		salt_length = 5
		return ''.join(random.choice(string.letters) for _ in range(salt_length))

	@staticmethod
	def hash_email_pw(email, pw, salt=None):
		if salt is None:
			salt = User.make_salt()
		return ''.join([hashlib.sha256(email+pw+salt).hexdigest(),'|',salt])

	@staticmethod
	def email_exists(email):
		user = db.GqlQuery("SELECT * FROM User WHERE email = '%s'" % email).get()
		return user != None

	@staticmethod
	def validate_email_pw(email, pw):
		user = db.GqlQuery("SELECT * FROM User WHERE email = '%s'" % email).get()
		if user == None:
			return None
			
		pos = user.email_pw_salt.find('|')
		salt = user.email_pw_salt[pos+1:]
		if User.hash_email_pw(email, pw, salt=salt) == user.email_pw_salt:
			return user.key().id()

	def store(self, password):
		self.email_pw_salt = User.hash_email_pw(self.email, password)
		self.put()