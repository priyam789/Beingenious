import re
from datetime import date
from base import *


class CoursePage(Handler):
	def get(self):
		course_code = self.request.get('code')
		course_details = Course.get_details_course(course_code)
		if(course_details == None):
			self.error(404)
		else:
			self.render('course_page.html', course_details = course_details)
	
	def post(self):
		course_code = self.request.get('code')
		course_details = Course.get_details_course(course_code)
		curr_user = self.cookie_user()
		if(curr_user == None):
			self.redirect('/login?pane=signin')
		elif(course_details == None):
			self.error(404)
		else:
			# if(course_details.author == curr_user.email):
			# 	sign_in_error = "You can not enroll for a course started by yourself. It is common sense."
			# 	self.render('course_page.html',course_details = course_details,sign_in_error = sign_in_error)
			# else:
			user_already_reg = User_Course.get_courses_reg(curr_user.email)
			# improve this functionality by making an alert option and giving the option to resume learning and probably this if condition is a costly databse operation
			found = False
			for course_already in user_already_reg:
				if(course_details.code == course_already.code):
					found = True
			if(found):
				sign_in_error = "You are already enrolled for this course"
				self.render('course_page.html',course_details = course_details,sign_in_error = sign_in_error)
			else:
				user_course = User_Course(user = curr_user.email,code = course_details.code)
				user_course.put()
				self.write("You are enrolled for the course")
	