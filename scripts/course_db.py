import random
import string
import hashlib

from google.appengine.ext import ndb
from user_db import *

# This is the model class for courses database
class Course(ndb.Model):
	code = ndb.StringProperty(required = True)
	ctitle = ndb.StringProperty(required = True)
	overview = ndb.TextProperty()
	author = ndb.StringProperty(required = True)
	organization = ndb.StringProperty()
	date_start = ndb.DateProperty(required = True)
	date_end = ndb.DateProperty(required = True)
	area = ndb.StringProperty(required = True)
	level = ndb.StringProperty(required = True)
	overview_video = ndb.JsonProperty()
	contents = ndb.JsonProperty()
	discussion = ndb.JsonProperty()
	type_course = ndb.StringProperty()

	@staticmethod
	def parent_key():
		return ndb.Key('Course', 'Instructor')

	@staticmethod
	def get_category_events(category):
		categ_event_list = ndb.gql("SELECT * FROM Course WHERE area = '%s'" % category)
		return categ_event_list 

	@staticmethod
	def get_courses_floated(email):
		course_float_list = Course.query(Course.author == email, ancestor=Course.parent_key())
		return course_float_list

	@staticmethod
	def get_num_courses():
		total = ndb.gql("SELECT * FROM Course ").count()
		return total

	@staticmethod
	def get_details_course(code):
		course_para = Course.query(Course.code == code, ancestor=Course.parent_key()).get()
		return course_para

	@staticmethod
	def verify_author(code, email):
		course_details = Course.query(Course.code == code, Course.author == email, ancestor=Course.parent_key()).get()
		return course_details

	def get_author_name(self):
		author = User.get_by_email(self.author)
		return ''.join([author.fname, ' ', author.lname])

	def is_event(self):
		if self.type_course == 'event':
			return True
		return False
