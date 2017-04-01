import os
import hmac

import webapp2
import jinja2

from database import *

template_dir = os.path.join(os.path.dirname(__file__), '../templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)

class Handler(webapp2.RequestHandler):
	secret = 'davinciscode'
	def write(self, *a, **kw):
		self.response.write(*a, **kw)

	def render_str(self, template, **kw):
		user = self.cookie_user()
		t = jinja_env.get_template(template)
		return t.render(user=user, **kw)

	def render(self, template, **kw):
		self.write(self.render_str(template, **kw))

	@staticmethod
	def hash_cookie(s = None):
		hash_val = ''
		if s is not None:
			hash_val = ''.join([s, '|', hmac.new(Handler.secret, s).hexdigest()])
		return hash_val

	@staticmethod
	def validate_cookie(val, cookie_val):
		return Handler.hash_cookie(val) == cookie_val

	def set_cookie(self, user_id = None):
		user_id = str(user_id)
		hashed_user_id = Handler.hash_cookie(user_id)
		self.response.headers.add_header('Set-Cookie', 'user_id=%s; Path=/' %hashed_user_id)

	def cookie_user(self):
		cookie_user = self.request.cookies.get('user_id')
		if cookie_user is None:
			return None

		pos = cookie_user.find('|')
		user_id = cookie_user[:pos]
		if Handler.validate_cookie(user_id, cookie_user) and user_id.isdigit():
			user_id = int(user_id)
			user = User.get_by_id(user_id)
			return user
