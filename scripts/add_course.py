import re
from datetime import date
from base import *
def generate_code(area):
		total_courses = Course.get_num_courses()
		answer = area[0]+"OL"+str(100+total_courses)
		return answer

class Add_course(Handler):
	def get(self):
		self.render('course_create.html')
	def post(self):
		self.add_course()
	def add_course(self):
		title = self.request.get('title')
		desc = self.request.get('overview')
		sdate = self.request.get('start_date')
		edate = self.request.get('end_date')
		area = self.request.get('area')
		author = self.cookie_user()
		empty_title = False
		invalid_dates = False
		empty_title_error = ""
		invalid_date_error = ""
		#  checking for empty fields or invalid dates
		if(title == ""):
			empty_title_error = "Title can not be left blank"
			empty_title = True
		if(edate == "" or sdate == ""):
			invalid_dates = True
			invalid_date_error = "Both the start and end dates need to be specified"
		if(sdate >= edate):
			invalid_dates = True
			invalid_date_error = "End date needs to exceed the start date"
		course_code = generate_code(area)
		# self.write(course_code)

		# displaying the page based on whether the dates are valid or not
		if(not(invalid_dates or empty_title)):
			sdate_arr = sdate.split('-')
			edate_arr = edate.split('-')
			sdate_db = date(int(sdate_arr[0]),int(sdate_arr[1]),int(sdate_arr[2]))
			edate_db = date(int(edate_arr[0]),int(edate_arr[1]),int(edate_arr[2]))
			course = Course(ctitle = title, overview = desc, author = author.email, date_start = sdate_db, date_end = edate_db, area = area,code = course_code)
			course.put()
			self.write("Course added successfully")
		else:
			self.render('course_create.html',title = title,overview = desc,start_date = sdate,end_date = edate,area = area,empty_title_error = empty_title_error,invalid_date_error = invalid_date_error)
