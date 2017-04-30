import re
from datetime import date
from datetime import datetime
from base import *


class ParticipantsPage(Handler):

	def get(self,course_code):
		# course_code = self.request.get('code')
		user = self.cookie_user()
		if user is None:
			self.redirect('/login?pane=signin')
			return
		course = Course.verify_author(course_code, user.email)
		course_detail = course
		if( course is None ):
			self.redirect('/courses/%s' %course_code)
		else:
			(user_namelist,user_gradelist) = User_Course.get_users_enrolled(course_code)
			
		self.render('participants.html',course_code = course_code,course = course_detail,user_namelist = zip(user_namelist,user_gradelist),user_gradelist = user_gradelist)

