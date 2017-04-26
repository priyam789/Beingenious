from base import *

class EditCourse(Handler, blobstore_handlers.BlobstoreUploadHandler):
	form_fields = ['module_name', 'subtitle', 'upload', 'file', 'link']
	def render_page(self, template, course_code, **kw):
		upload_url = blobstore.create_upload_url('/editcourse/%s' %course_code)
		self.render(template, upload_url = upload_url, tag='initiator', **kw)

	def get(self, course_code):
		user = self.cookie_user()
		course = Course.verify_author(course_code, user.email)
		if course is None:
			self.redirect('/courses/%s' %course_code)

		self.render_page('edit_course.html', course_code, course = course)

	def post(self, course_code):
		user = self.cookie_user()
		course = Course.verify_author(course_code, user.email)
		if course is None:
			self.redirect('/courses/%s' %course_code)

		form_data = self.get_form_data()
		(error_present, error) = self.error_check(form_data)

		if error_present:
			render_data = dict(form_data, **error)
			self.render_page('edit_course.html', course_code, course = course, **render_data)
		else:
			module_id = len(course.contents)+1
			module = {'id':module_id, 'name':form_data['module_name'], 'lessons':[]}
			lesson = self.construct_lesson(form_data)
			module['lessons'].append(lesson)
			course.contents.append(module)
			course.put()
			self.redirect('/editcourse/%s' %course_code)

	def get_form_data(self):
		form_data = dict()
		for field in EditCourse.form_fields:
			form_data[field] = self.request.get(field, '')
		return form_data

	def error_check(self, form_data):
		error_present = False
		error = dict()
		error['empty_title'] = ''
		error['empty_subtitle'] = ''
		error['file_error'] = ''
		
		#  checking for empty fields
		if(form_data['module_name'] == ''):
			error['empty_title'] = 'Module name can not be left blank'
			error_present = True

		if(form_data['subtitle'] == ''):
			error['empty_subtitle'] = 'Lesson Title can not be left blank'
			error_present = True

		if(form_data['upload'] == 'file' and form_data['file'] == ''):
			error['file_error'] = 'No file uploaded'
			error_present = True

		elif(form_data['upload'] == 'link' and form_data['link'] == ''):
			error['file_error'] = 'No link to video given'
			error_present = True

		return (error_present, error)

	def construct_lesson(self, form_data):
		lesson = dict()
		if(form_data['upload'] == 'file'):
			upload = self.get_uploads()[0]
			video_link = '/view_video/%s' %str(upload.key())
			lesson = {'type':'blob', 'blob_key':str(upload.key()), 'link':video_link}
		elif(form_data['upload'] == 'link'):
			lesson = {'type':'link', 'link':form_data['link']}

		return lesson