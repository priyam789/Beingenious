import random
import string
import hashlib

from google.appengine.ext import db

def make_salt():
	salt_length = 5
	return ''.join(random.choice(string.letters) for _ in range(salt_length))

def hash_email_pw(email, pw, salt=None):
	if salt is None:
		salt = make_salt()
	return ''.join([hashlib.sha256(email+pw+salt).hexdigest(),'|',salt])

class Candidate(db.Model):
	fname = db.StringProperty(required = True)
	lname = db.StringProperty(required = True)
	email = db.StringProperty(required = True)
	email_pw_salt = db.StringProperty(required = True)
	created = db.DateTimeProperty(auto_now_add = True)

	def store(self, password):
		self.email_pw_salt = hash_email_pw(self.email, password)
		candidate = db.GqlQuery("SELECT * FROM Candidate WHERE email = '%s'" % self.email).get()
		if candidate is not None:
			candidate.fname = self.fname
			candidate.lname = self.lname
			candidate.email_pw_salt = self.email_pw_salt
			candidate.put()
		else:
			self.put()
		
		verification_link = ''.join(['/activate?link=',self.email_pw_salt])
		return verification_link

	@staticmethod
	def get_by_activation_link(link):
		candidate = db.GqlQuery("SELECT * FROM Candidate WHERE email_pw_salt = '%s'" % link).get()
		return candidate

class User(db.Model):
	fname = db.StringProperty(required = True)
	lname = db.StringProperty(required = True)
	email = db.StringProperty(required = True)
	email_pw_salt = db.StringProperty(required = True)
	hashed_link = db.StringProperty(required = True)

	@staticmethod
	def get_by_email(email):
		user = db.GqlQuery("SELECT * FROM User WHERE email = '%s'" % email).get()
		return user

	@staticmethod
	def email_exists(email):
		user = User.get_by_email(email)
		return user != None

	@staticmethod
	def validate_email_pw(email, pw):
		user = User.get_by_email(email)
		if user == None:
			return None
			
		pos = user.email_pw_salt.find('|')
		salt = user.email_pw_salt[pos+1:]
		if hash_email_pw(email, pw, salt=salt) == user.email_pw_salt:
			return user.key().id()

	@classmethod
	def store(cls, candidate):
		user = cls(fname = candidate.fname,
					lname = candidate.lname,
					email = candidate.email,
					email_pw_salt = candidate.email_pw_salt)
		candidate.key.delete()
		user.put()

	@staticmethod
	def activate(link):
		candidate = Candidate.get_by_activation_link(link)
		if candidate is not None:
			User.store(candidate)
			return 0