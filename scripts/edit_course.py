from base import *

class EditCourse(Handler, blobstore_handlers.BlobstoreUploadHandler):
	form_fields = ['edit_module', 'module_name', 'subtitle', 'lesson_format', 'description', 'upload', 'file', 'link', 'quiz_format', 'question', 'num_options']
	def render_page(self, template, course_code, **kw):
		current_url = '/editcourse/%s' %course_code
		upload_url = blobstore.create_upload_url(current_url)
		self.render(template, upload_url = upload_url, tag='initiator', **kw)

	def get(self, course_code):
		user = self.cookie_user()
		course = Course.verify_author(course_code, user.email)
		if course is None:
			self.redirect('/courses/%s' %course_code)
		edit_module = self.request.get('module', '')
		try:
			edit_module = int(edit_module)
		except:
			edit_module = -1
		if edit_module >= len(course.contents):
			edit_module = -1
		self.render_page('edit_course.html', course_code, course = course, edit_module = edit_module)

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
		
		elif form_data['edit_module'] == -1:
			module_id = len(course.contents)
			module = {'id':module_id, 'name':form_data['module_name'], 'lessons':[]}
			lesson = self.construct_lesson(form_data)
			module['lessons'].append(lesson)
			course.contents.append(module)
			course.put()
			self.redirect('/editcourse/%s?module=%s' %(course_code, str(module_id)))
		
		else:
			module = course.contents[form_data['edit_module']]
			lesson_id = len(module['lessons'])
			lesson = self.construct_lesson(form_data, lesson_id)
			module['lessons'].append(lesson)
			course.contents[form_data['edit_module']] = module
			course.put()
			self.redirect('/editcourse/%s?module=%s' %(course_code, form_data['edit_module']))

	def get_form_data(self):
		form_data = dict()
		for field in EditCourse.form_fields:
			form_data[field] = self.request.get(field, '')
		form_data['edit_module'] = int(form_data['edit_module'])

		if(form_data['lesson_format'] == 'quiz'):
			quiz_format = form_data['quiz_format']
			form_data['num_options'] = int(form_data['num_options'])
			form_data['options'] = []
			for i in range(1, form_data['num_options']+1):
				form_data['options'].append(self.request.get(quiz_format+'_'+str(i)))
			form_data['correct'] = self.request.get_all(quiz_format+'_correct')
		return form_data

	def error_check(self, form_data):
		error_present = False
		error = dict()
		error['empty_title'] = ''
		error['empty_subtitle'] = ''
		error['file_error'] = ''
		
		#  checking for empty fields
		if(form_data['edit_module'] == -1 and form_data['module_name'] == ''):
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

	def construct_lesson(self, form_data, lesson_id=0):
		lesson = {'id': lesson_id, 'name':form_data['subtitle'], 'description': form_data['description']}
		if(form_data['lesson_format'] == 'lecture' and form_data['upload'] == 'file'):
			upload = self.get_uploads()[0]
			lesson['type'] = 'blob'
			lesson['blob_key'] = str(upload.key())
			lesson['link'] = '/view_video/%s' %str(upload.key())

		elif(form_data['lesson_format'] == 'lecture' and form_data['upload'] == 'link'):
			lesson['type'] = 'link'
			lesson['link'] = form_data['link']

		elif(form_data['lesson_format'] == 'quiz'):
			lesson['type'] = 'quiz'
			lesson['quiz_format'] = form_data['quiz_format']
			lesson['question'] = form_data['question']
			lesson['options'] = form_data['options']
			lesson['correct'] = form_data['correct']

		return lesson