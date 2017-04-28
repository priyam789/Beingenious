import random
import string
import hashlib

from google.appengine.ext import ndb
from course_db import *

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

	@classmethod
	def enroll_user_course(cls,email,code):
		course_registration = User_Course.query(User_Course.user == email,User_Course.code == code,ancestor = User_Course.parent_key()).get()
		if(course_registration is None):
			user_course = cls(user = email,code = code)
			user_course.put()

	@staticmethod
	def get_courses_reg(email):
		course_reg_list = User_Course.query(User_Course.user == email)
		courses = []
		for course_reg in course_reg_list:
			detail = Course.get_details_course(course_reg.code)
			courses.append(detail)
		return courses

	@staticmethod
	def verify_user(code, email):
		user_course = User_Course.query(User_Course.code == code, User_Course.user == email, ancestor=User_Course.parent_key()).get()
		if(user_course is None):
			return user_course
		else:
			course_detail = Course.get_details_course(user_course.code)
			return course_detail

	# @staticmethod
	# def get_num_courses():
	# 	total = ndb.gql("SELECT * FROM Course ").count()
	# 	return total

	# @staticmethod
	# def get_details_course(code):
	# 	course_para = ndb.gql("SELECT * FROM Course WHERE ctitle ='%s'" % code).get()
	# 	return course_para