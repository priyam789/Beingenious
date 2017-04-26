import random
import string
import hashlib

from google.appengine.ext import ndb

class User_Course(ndb.Model):
	user = ndb.StringProperty(required = True)
	code = ndb.StringProperty(required = True)
	
	@staticmethod
	def parent_key():
		return ndb.Key('Course','Instructor')
	# @staticmethod
	# def get_category_events(category):
	# 	categ_event_list = ndb.gql("SELECT * FROM Course WHERE area = '%s'" % category).run()
	# 	return categ_event_list 

	@staticmethod
	def get_courses_reg(email):
		course_reg_list = User_Course.query(User_Course.user == email,ancestor = User_Course.parent_key())
		return course_reg_list

	# @staticmethod
	# def get_num_courses():
	# 	total = ndb.gql("SELECT * FROM Course ").count()
	# 	return total

	# @staticmethod
	# def get_details_course(code):
	# 	course_para = ndb.gql("SELECT * FROM Course WHERE ctitle ='%s'" % code).get()
	# 	return course_para