import random
import string
import hashlib

from google.appengine.ext import db

class Course(db.Model):
	ctitle = db.StringProperty(required = True)
	overview = db.StringProperty()
	author = db.StringProperty(required = True)
	date_start = db.DateProperty(required = True)
	date_end = db.DateProperty(required = True)
	area = db.StringProperty(required = True)
	code = db.StringProperty()

	# @staticmethod
	# def make_salt():
	# 	salt_length = 5
	# 	return ''.join(random.choice(string.letters) for _ in range(salt_length))

	# @staticmethod
	# def hash_email_pw(email, pw, salt=None):
	# 	if salt is None:
	# 		salt = User.make_salt()
	# 	return ''.join([hashlib.sha256(email+pw+salt).hexdigest(),'|',salt])

	@staticmethod
	def get_category_events(category):
		categ_event_list = db.GqlQuery("SELECT * FROM Course WHERE area = '%s'" % category).run()
		return categ_event_list 

	@staticmethod
	def get_courses_floated(email):
		course_float_list = db.GqlQuery("SELECT * FROM Course WHERE author = '%s'" % email).run()
		return course_float_list

	@staticmethod
	def get_num_courses():
		total = db.GqlQuery("SELECT * FROM Course ").count()
		return total

	@staticmethod
	def get_details_course(code):
		course_para = db.GqlQuery("SELECT * FROM Course WHERE ctitle ='%s'" % code).get()
		return course_para

	# @staticmethod
	# def validate_email_pw(email, pw):
	# 	user = db.GqlQuery("SELECT * FROM User WHERE email = '%s'" % email).get()
	# 	if user == None:
	# 		return None
			
	# 	pos = user.email_pw_salt.find('|')
	# 	salt = user.email_pw_salt[pos+1:]
	# 	if User.hash_email_pw(email, pw, salt=salt) == user.email_pw_salt:
	# 		return user.key().id()

	# def store(self, password):
	# 	self.email_pw_salt = User.hash_email_pw(self.email, password)
	# 	self.put()