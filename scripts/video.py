from base import *

class ServeVideo(blobstore_handlers.BlobstoreDownloadHandler):
	def get(self, blob_key):
		self.send_blob(blob_key)

class SubmitPage(Handler, blobstore_handlers.BlobstoreUploadHandler):
	def get(self, course_code, module_id, lesson_id):
		user = self.cookie_user()
		if user is None:
			self.redirect('/login?pane=signin')
		user_course = User_Course.check_user_enrolled(course_code, user.email)

		if user_course is None:
			self.render('message.html', message='You are not enrolled for this course')
		else:
			current_url = '/submit/%s/%s/%s' %(course_code, module_id, lesson_id)
			upload_url = blobstore.create_upload_url(current_url)
			self.render('submit.html', upload_url=upload_url)

	def post(self, course_code, module_id, lesson_id):
		user = self.cookie_user()
		if user is None:
			self.redirect('/login?pane=signin')
		user_course = User_Course.check_user_enrolled(course_code, user.email)
		if user_course is None:
			self.render('message.html', message='You are not enrolled for this course')
		else:
			upload = self.get_uploads()[0]
			submit_url = '/view_video/%s' %(str(upload.key()))
			User_Course.add_grade_student(course_code, int(module_id), int(lesson_id), user.email, marks=0, submit=submit_url)
			self.redirect('/courses/%s?module=%s' %(course_code, module_id))


class EventSubmitPage(Handler, blobstore_handlers.BlobstoreUploadHandler):
	def get(self, course_code):
		user = self.cookie_user()
		if user is None:
			self.redirect('/login?pane=signin')
		user_course = User_Course.check_user_enrolled(course_code, user.email)

		if user_course is None:
			self.render('message.html', message='You are not enrolled for this course')
		else:
			current_url = '/submit/%s' %(course_code)
			upload_url = blobstore.create_upload_url(current_url)
			self.render('submit.html', upload_url=upload_url)

	def post(self, course_code):
		user = self.cookie_user()
		if user is None:
			self.redirect('/login?pane=signin')
		user_course = User_Course.check_user_enrolled(course_code, user.email)
		if user_course is None:
			self.render('message.html', message='You are not enrolled for this course')
		else:
			upload = self.get_uploads()[0]
			submit_url = '/view_video/%s' %(str(upload.key()))
			user_course.grades['submission'] = submit_url
			user_course.grades['marks'] = 0
			user_course.put()
			self.redirect('/courses/%s?tag=benefitter' %course_code)


