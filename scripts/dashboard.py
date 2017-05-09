import re
from datetime import date
from base import *

# This class handles the display of the dashboard
class DashboardPage(Handler):	
	def get(self):
		user = self.cookie_user()
		if user is None:
			self.redirect('/login?pane=signin')
			return
		author = self.cookie_user()
		# self.write(author.email)
		course_floated = Course.get_courses_floated(author.email)
		course_registered = User_Course.get_courses_reg(author.email)

		self.render('dashboard.html',course_float_list = course_floated,courses = course_registered)
