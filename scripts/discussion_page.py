import re
from datetime import date
from datetime import datetime
from base import *

def format_time(time):
	date_string = str(time.day)+"/"+str(time.month)+"/"+str(time.year)+"   "+str(time.hour)+":"+str(time.minute)
	return date_string

class DiscussionPage(Handler):

	def get(self,course_code):
		# course_code = self.request.get('code')
		user = self.cookie_user()
		tag = self.request.get('tag')
		if tag != 'initiator':
			tag = 'benefitter'
		if user is None:
			self.redirect('/login?pane=signin')
		else:
			course = Course.verify_author(course_code, user.email)
			course_detail = course
			if( course is None ):
				user_course = User_Course.verify_user(course_code,user.email)
				if(user_course is None):
					self.redirect('/courses?code=%s' %course_code)
				else:
					course_detail = user_course
					self.render('discussion.html',course_code = course_code,course = course_detail, dtag=tag)
			else:
				self.render('discussion.html',course_code = course_code,course = course_detail, dtag=tag)

	def post(self,course_code):
		form_name = self.request.get('post_R')
		tag = self.request.get('tag')
		if tag != 'initiator':
			tag = 'benefitter'
		if form_name == "Post":
			query_title = self.request.get('query_title')
			query_content = self.request.get('query_desc')
			user = self.cookie_user()
			course_details = Course.get_details_course(course_code)
			# if query_title == "":
			# 	error = "Query cannot be posted without a title"
			# 	self.render('discussion.html',course_code = course_code,course = course_details,error=error)
			# else:
			t = datetime.now()
			curr_time = format_time(t)
			query_id = len(course_details.discussion)
			single_query = self.construct_query(query_title,query_content,query_id,user,curr_time)
			course_details.discussion.append(single_query)
			course_details.put()
			self.render('discussion.html',course_code = course_code,course = course_details, dtag=tag)
		else:
			q_id = self.request.get('reply_form_hidden')
			reply_content = self.request.get('reply_desc_'+q_id)
			user = self.cookie_user()
			course_details = Course.get_details_course(course_code)
			if reply_content:
				t = datetime.now()
				curr_time = format_time(t)
				reply_id = len(course_details.discussion[int(q_id)]['reply'])
				single_reply = self.construct_reply(reply_content,reply_id,user,curr_time)
				course_details.discussion[int(q_id)]['reply'].append(single_reply)
				course_details.put()
			self.render('discussion.html',course_code = course_code,course = course_details, dtag=tag)
	
	def construct_query(self,title,content,qid,user,time):
		query = dict()
		query = {'query_id':qid,'title':title,'content':content,'user':user.email,'time':time,'reply':[]}
		return query

	def construct_reply(self,content,r_id,user,time):
		reply = dict()
		reply = {'reply_id':r_id,'content':content,'user':user.email,'time':time}
		return reply