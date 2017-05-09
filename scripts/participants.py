import re
from datetime import date
from datetime import datetime
from base import *

# This class handles the display of the enrolled participants' information
class ParticipantsPage(Handler):

	def get(self,course_code):
		# course_code = self.request.get('code')
		user = self.cookie_user()
		if user is None:
			self.redirect('/login?pane=signin')
			return
		else:
			course = Course.verify_author(course_code, user.email)
			if( course is None ):
				self.redirect('/courses/%s' %course_code)
			else:
				(user_namelist,user_gradelist) = User_Course.get_users_enrolled(course_code)
				
			self.render('participants.html',course_code = course_code,course = course,user_namelist = zip(user_namelist,user_gradelist),tag='initiator', dtag='initiator')

	def post(self, course_code):
		user = self.cookie_user()
		if user is None:
			self.redirect('/login?pane=signin')
			return
		else:
			course = Course.verify_author(course_code, user.email)
			if( course is None ):
				self.redirect('/courses/%s' %course_code)
			else:
				user_course_key = self.request.get('key')
				marks = int(self.request.get('marks'))
				user_course = User_Course.get_by_id(int(user_course_key),parent=User_Course.parent_key())
				user_course.grades['marks'] = marks
				user_course.put()
				self.redirect('/participants/%s' %(course_code))

# This class handles the display and editing of the enrolled participants' grades
class ViewGradesPage(Handler):

	def get(self, user_course_key, course_code):
		# course_code = self.request.get('code')
		user = self.cookie_user()
		if user is None:
			self.redirect('/login?pane=signin')
		else:
			tag = self.request.get('tag')
			if(tag != 'initiator'):
				tag = 'benefitter'

			course = None

			if(tag != 'initiator'):
				course = User_Course.verify_user(course_code, user.email)
			else:
				course = Course.verify_author(course_code, user.email)

			if( course is None ):
				self.redirect('/courses/%s' %course_code)

			elif (course.type_course == 'event' and tag == 'benefitter'):
				user_course = User_Course.get_by_id(int(user_course_key),parent=User_Course.parent_key())
				user_info = User.get_by_email(user_course.user)
				self.render('grade_event.html',course_code = course_code,course = course, tag=tag, dtag=tag,
							user_info = user_info,user_gradelist = user_course.grades, user_course = user_course)
			else:
				user_course = User_Course.get_by_id(int(user_course_key),parent=User_Course.parent_key())
				user_info = User.get_by_email(user_course.user)
				self.render('grades.html',course_code = course_code,course = course, tag=tag, dtag=tag,
							user_info = user_info,user_gradelist = user_course.grades, user_course = user_course)

	def post(self, user_course_key, course_code):
		user = self.cookie_user()
		if user is None:
			self.redirect('/login?pane=signin')
		else:
			course = Course.verify_author(course_code, user.email)
			if( course is None ):
				self.redirect('/courses/%s' %course_code)
			else:
				user_course = User_Course.get_by_id(int(user_course_key),parent=User_Course.parent_key())
				module_id = int(self.request.get('module_id'))
				lesson_id = int(self.request.get('lesson_id'))
				marks = int(self.request.get('marks'))
				user_course.grades[str((module_id, lesson_id))]['obt_marks'] = marks
				user_course.put()

				user_info = User.get_by_email(user_course.user)
				self.render('grades.html',course_code = course_code,course = course, tag='initiator', dtag='initiator',
							user_info = user_info,user_gradelist = user_course.grades, user_course = user_course)

