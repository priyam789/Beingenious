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