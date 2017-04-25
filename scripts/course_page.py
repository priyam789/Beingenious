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
			video_link = '/view_video/%s' %course_details.overview_video['blob_key']
			self.render('course_page.html', course_details = course_details, video_link = video_link)
	
	def post(self):
		course_code = self.request.get('code')
		course_details = Course.get_details_course(course_code)
		curr_user = self.cookie_user()
		if(curr_user == None):
			self.redirect('/login?pane=signin')
		elif(course_details == None):
			self.error(404)
		else:
			self.write('You are enrolled for the course')
	