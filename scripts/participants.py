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

		else:

			course = Course.verify_author(course_code, user.email)
			if( course is None ):
				self.redirect('/courses/%s' %course_code)
			else:
				(user_namelist,user_gradelist) = User_Course.get_users_enrolled(course_code)
				
			self.render('participants.html',course_code = course_code,course = course,user_namelist = zip(user_namelist,user_gradelist))


class ViewGradesPage(Handler):

	def get(self, user_course_key, course_code):
		# course_code = self.request.get('code')
		user = self.cookie_user()
		if user is None:
			self.redirect('/login?pane=signin')

		else:

			course = Course.verify_author(course_code, user.email)
			
			if( course is None ):
				self.redirect('/courses/%s' %course_code)
			else:
				user_course = User_Course.get_by_id(int(user_course_key),parent=User_Course.parent_key())
				user_info = User.get_by_email(user_course.user)
				
			self.render('grades.html',course_code = course_code,course = course,user_info = user_info,user_gradelist = user_course.grades)

