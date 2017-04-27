import re
from datetime import date
from base import *

class DashboardPage(Handler):	#TODO: will go in a separate file
	def get(self):
		author = self.cookie_user()
		# self.write(author.email)
		course_floated = Course.get_courses_floated(author.email)
		course_registered = User_Course.get_courses_reg(author.email)

		self.render('dashboard.html',course_float_list = course_floated,courses = course_registered)
