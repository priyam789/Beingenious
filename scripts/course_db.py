import random
import string
import hashlib

from google.appengine.ext import db

class Course(db.Model):
	ctitle = db.StringProperty(required = True)
	code = db.StringProperty(required = True)
	overview = db.TextProperty()
	author = db.StringProperty(required = True)
	date_start = db.DateProperty(required = True)
	date_end = db.DateProperty(required = True)
	area = db.StringProperty(required = True)
	level = db.StringProperty(required = True)

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