import re
from datetime import date
from base import *

area_code_map = {'Dance':'DAL', 'Music':'MUL', 'Theatre':'THL', 'Literature':'LIT', 'Quiz & Debate':'QDL', 'Academia':'ACL'}
def generate_code(area):
		total_courses = Course.get_num_courses()
		answer = area_code_map[area]+str(100+total_courses)
		return answer

class AddCourse(Handler, blobstore_handlers.BlobstoreUploadHandler):
	form_fields = ['title', 'organization', 'overview',
					'start_date', 'end_date', 'area', 'level',
					'upload', 'file', 'link']

	def render_form(self, **kw):
		upload_url = blobstore.create_upload_url('/create_course')
		self.render('course_create.html', upload_url=upload_url, **kw)

	def get(self):
		user = self.cookie_user()
		if user is None:
			self.redirect('/login?pane=signin')
		self.no_cache()

		self.render_form()

	def post(self):
		user = self.cookie_user()
		if user is None:
			self.redirect('/login?pane=signin')
		self.no_cache()

		form_data = self.get_form_data()
		error_present, error = self.error_check(form_data)

		if not error_present:
			self.add_course(form_data)

		else:
			render_data = dict(form_data, **error)
			self.render_form(**render_data)
			

	def get_form_data(self):
		form_data = dict()
		for field in AddCourse.form_fields:
			form_data[field] = self.request.get(field, '')
		return form_data
		
	def error_check(self, form_data):
		error_present = False
		error = dict()
		error['empty_title'] = ''
		error['invalid_date'] = ''
		error['file_error'] = ''
		
		#  checking for empty fields or invalid dates
		if(form_data['title'] == ''):
			error['empty_title'] = 'Title can not be left blank'
			error_present = True
		if(form_data['start_date'] == '' or form_data['end_date'] == ''):
			error['invalid_date'] = 'Both the start and end dates need to be specified'
			error_present = True
		elif(form_data['start_date'] >= form_data['end_date']):
			error['invalid_date'] = 'End date needs to exceed the start date'
			error_present = True

		if(form_data['upload'] == 'file' and form_data['file'] == ''):
			error['file_error'] = 'No file uploaded'
			error_present = True
		elif(form_data['upload'] == 'link' and form_data['link'] == ''):
			error['file_error'] = 'No link to video given'
			error_present = True

		return (error_present, error)

	def add_course(self, form_data):
		author = self.cookie_user()
		course_code = generate_code(form_data['area'])
		
		sdate_arr = form_data['start_date'].split('-')
		edate_arr = form_data['end_date'].split('-')
		sdate_db = date(int(sdate_arr[0]),int(sdate_arr[1]),int(sdate_arr[2]))
		edate_db = date(int(edate_arr[0]),int(edate_arr[1]),int(edate_arr[2]))
		course = Course(parent = Course.parent_key(), code = course_code,
						ctitle = form_data['title'], overview = form_data['overview'],
						author = author.email, organization = form_data['organization'],
						date_start = sdate_db, date_end = edate_db,
						area = form_data['area'], level = form_data['level'])

		if(form_data['upload'] == 'file'):
			upload = self.get_uploads()[0]
			video_link = '/view_video/%s' %str(upload.key())
			course.overview_video = {'type':'blob', 'blob_key':str(upload.key()), 'link':video_link}
		elif(form_data['upload'] == 'link'):
			course.overview_video = {'type':'link', 'link':form_data['link']}
		course.put()
		
		self.redirect('/courses?code=%s' %course_code)