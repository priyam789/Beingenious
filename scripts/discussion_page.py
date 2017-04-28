import re
from datetime import date
from base import *



class DiscussionPage(Handler):

	def get(self,course_code):
		# course_code = self.request.get('code')
		user = self.cookie_user()
		course = Course.verify_author(course_code, user.email)
		course_detail = course
		if( course is None ):
			user_course = User_Course.verify_user(course_code,user.email)
			if(user_course is None):
				self.redirect('/courses/%s' %course_code)
			else:
				course_detail = user_course
		self.render('discussion.html',course_code = course_code,course = course_detail)

	def post(self,course_code):
		query_title = self.request.get('query_title')
		query_content = self.request.get('query_desc')
		user = self.cookie_user()
		course_details = Course.get_details_course(course_code)
		error = ""
		if query_title == "":
			error = "Query cannot be posted without a title"
			self.render('discussion.html',course_code = course_code,course = course_details,error=error)
		else:
			single_query = self.construct_query(query_title,query_content,user)
			course_details.discussion.append(single_query)
			course_details.put()
			self.render('discussion.html',course_code = course_code,course = course_details)

	def construct_query(self,title,content,user):
		query = dict()
		query = {'title':title,'content':content,'user':user.email,'reply':[]}
		return query