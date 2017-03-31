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
	def hash_email_pw(email, pw):
		salt = User.make_salt()
		return ''.join([hashlib.sha256(email+pw+salt).hexdigest(),'|',salt])

	@staticmethod
	def email_exists(email):
		user = db.GqlQuery("SELECT * FROM User WHERE email = '%s'" % email).get()
		return user != None

	def store(self, password):
		self.email_pw_salt = User.hash_email_pw(self.email, password)
		self.put()