from datetime import date
from base import *


class CoursePage(Handler):
	def get(self):
		course_code = self.request.get('code')
		tag = self.request.get('tag', 'benefitter')
		if (tag != 'initiator' and tag != 'benefitter'):
			self.redirect('/courses?code=%s' %course_code)
		course_details = Course.get_details_course(course_code)
		if(course_details == None):
			self.error(404)
		else:
			self.render('course_page.html', course_details = course_details, tag = tag)
	
class CourseMainPage(Handler):
	def get(self, course_code):
		user = self.cookie_user()
		if user is None:
			self.redirect('/login?pane=signin')

		else:
			tag = self.request.get('tag', 'benefitter')
			if (tag != 'initiator' and tag != 'benefitter'):
				self.redirect('/courses/%s' %course_code)

			course = Course.get_details_course(course_code)
			if course == None:
				self.redirect('/dashboard')
		

			if(tag == 'benefitter'):
				User_Course.enroll_user_course(user.email,course.code)

			show_module = 0
			show_lesson = 0
			if(show_module >= len(course.contents) or show_lesson >= len(course.contents[0]['lessons'])):
				show_module = -1
				show_lesson = -1
			self.render('course_main_page.html', course = course, tag = tag,
					show_module = show_module, show_lesson = show_lesson)

	def post(self, course_code):
		correct = self.request.get("correct")
		module_id = int(self.request.get('module_id'))
		lesson_id = int(self.request.get("lesson_id"))
		user = self.cookie_user()
		

		if user is None:
			self.redirect('/login?pane=signin')

		else:
			course_details = User_Course.verify_user(course_code,user.email)
			if course_details:
				if correct =="0":
					User_Course.add_grade_student(course_code,module_id,lesson_id,user.email,marks=0)
				elif correct == "1":
					User_Course.add_grade_student(course_code,module_id,lesson_id,user.email,marks=course_details.contents[module_id]['lessons'][lesson_id]['max_marks'])
				self.redirect('/courses/%s' %course_code)

			else:
				self.redirect('/courses?code=%s' %course_code)