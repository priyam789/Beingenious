from base import *

class ProfilePage(Handler):
	def get(self):
		# user = self.cookie_user()
		self.render('profile.html')

class ChangePassword(Handler):
	def render_form(self, **kw):
		self.render('password.html', **kw)

	def get(self):
		self.render_form()

	def post(self):
		old_pass = self.request.get('old_pass')
		new_pass = self.request.get('new_pass')
		verify = self.request.get('verify')

		user = self.cookie_user()
		if user is None:
			self.redirect('/login?pane=signin')
		
