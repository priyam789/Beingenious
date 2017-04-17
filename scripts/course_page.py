import re
from datetime import date
from base import *


class CoursePage(Handler):
	def get(self):
		course_code = self.request.get("code")
		course_details = Course.get_details_course(course_code)
		sign_in_error = ""
		self.render('course_page.html',course_details = course_details,sign_in_error = sign_in_error)
	
	def post(self):
		course_code = self.request.get("code")
		course_details = Course.get_details_course(course_code)
		curr_user = self.cookie_user()
		if(curr_user == None):
			sign_in_error = "*Please sign in before joining the course"
			self.render('course_page.html',course_details = course_details,sign_in_error = sign_in_error)
		else:
			self.write("You are enrolled for the course")


	
	