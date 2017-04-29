import random
import string
import hashlib

from google.appengine.ext import ndb
from course_db import *

class User_Course(ndb.Model):
	user = ndb.StringProperty(required = True)
	code = ndb.StringProperty(required = True)
	grades = ndb.FloatProperty()

	@staticmethod
	def get_users_enrolled(code):
		user_list = User_Course.query(User_Course.code == code)
		user_enrolled = []
		for user_info in user_list:
			user_name = User.get_by_email(user_info.user)
			user_enrolled.append(user_name)
		return (user_enrolled,user_list)

	@staticmethod
	def parent_key():
		return ndb.Key('Course','Instructor')
	
	@classmethod
	def enroll_user_course(cls,email,code):
		course_registration = User_Course.query(User_Course.user == email, ancestor = User_Course.parent_key()).get()
		if course_registration == None:
			user_course = cls(parent = User_Course.parent_key(), user = email,code = code)
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

