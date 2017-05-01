import random
import string
import hashlib

from google.appengine.ext import ndb
from course_db import *

class User_Course(ndb.Model):
	user = ndb.StringProperty(required = True)
	code = ndb.StringProperty(required = True)
	grades = ndb.JsonProperty()

	@staticmethod
	def parent_key():
		return ndb.Key('Course','Instructor')
	
	@classmethod
	def enroll_user_course(cls,email,code):
		course_registration = User_Course.query(User_Course.user == email, User_Course.code == code, ancestor = User_Course.parent_key()).get()
		if course_registration == None:
			user_course = cls(parent = User_Course.parent_key(), user = email,code = code,grades = {})
			user_course.put()

	@staticmethod
	def get_users_enrolled(code):
		user_list = User_Course.query(User_Course.code == code)
		user_enrolled = []
		for user_info in user_list:
			user_name = User.get_by_email(user_info.user)
			user_enrolled.append(user_name)
		return (user_enrolled,user_list)
	@staticmethod
	def get_courses_reg(email):
		course_reg_list = User_Course.query(User_Course.user == email)
		courses = []
		for course_reg in course_reg_list:
			detail = Course.get_details_course(course_reg.code)
			courses.append(detail)
		return courses

	# @staticmethod
	# def add_grade(course_code,module_id,lesson):
	# 	user_list = User_Course.query(User_Course.code == course_code)
		
	# 	for user in user_list:
	# 		new_assignment = dict()
	# 		new_assignment[(module_id,lesson['id'])] = {'max_marks':lesson['max_marks'],'obt_marks':0,'submit':0}
	# 		user.grades=new_assignment
	# 		user.put()					

	@staticmethod
	def add_grade_student(course_code,module_id,lesson_id,user_email,marks=0, submit=''):
		user_spec = User_Course.query(User_Course.code == course_code, User_Course.user == user_email).get()
		if(str((module_id,lesson_id)) not in user_spec.grades or submit != ''):
			user_spec.grades[str((module_id,lesson_id))] = {}
			user_spec.grades[str((module_id,lesson_id))]['obt_marks'] = marks
			user_spec.grades[str((module_id,lesson_id))]['submit'] = submit
			user_spec.put()

	@staticmethod
	def verify_user(code, email):
		user_course = User_Course.query(User_Course.code == code, User_Course.user == email, ancestor=User_Course.parent_key()).get()
		if(user_course is None):
			return user_course
		else:
			course_detail = Course.get_details_course(user_course.code)
			return course_detail

	@staticmethod
	def check_user_enrolled(code, email):
		user_course = User_Course.query(User_Course.code == code, User_Course.user == email, ancestor=User_Course.parent_key()).get()
		return user_course

	# @staticmethod
	# def get_num_courses():
	# 	total = ndb.gql("SELECT * FROM Course ").count()
	# 	return total

	# @staticmethod
	# def get_details_course(code):
	# 	course_para = ndb.gql("SELECT * FROM Course WHERE ctitle ='%s'" % code).get()
	# 	return course_para

