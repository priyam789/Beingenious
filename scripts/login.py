import re
from datetime import date
from base import *
from mailing import *

DELIM = '-'


def validate_username(s):
	user_re = re.compile(r'^[a-zA-Z0-9]{3,20}$')
	if user_re.match(s) != None:
		return (True, '')
	else:
		return (False, 'Name should contain 3-20 alphanumeric characters')

def validate_password(s):
	password_re = re.compile(r'^.{3,20}$')
	if password_re.match(s) != None:
		return (True, '')
	else:
		return (False, 'Password should contain 3-20 characters')

def validate_oldpass(old_pass,user):
	old_pass_actual = user.email_pw_salt
	email = user.email
	pos = old_pass_actual.find(DELIM)
	salt = old_pass_actual[pos+1:]
	if hash_email_pw(email,old_pass,salt=salt) == old_pass_actual:
		return (True, '')
	else:
		return (False, 'Old Password entered is incorrect')

def validate_email(s):
	email_re = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
	if email_re.match(s) == None:
		return (False, 'This is an invalid email')
	elif User.email_exists(s):
		return (False, 'This email already has an account')
	else:
		return (True, '')

def match_passwords(s1, s2):
	if s1 == s2:
		return (True, '')
	else:
		return (False, "Passwords don't match")

class LoginPage(Handler):
	def render_page(self, pane, **kw):
		self.render('login.html', pane = pane, **kw)

	def get(self):
		pane = self.request.get('pane')
		self.render_page(pane=pane)

	def post(self):
		signin = self.request.get('signin')
		signup = self.request.get('signup')
		if signin:
			self.signin()
		elif signup:
			self.signup()

	def signup(self):
		fname = self.request.get('fname')
		lname = self.request.get('lname')
		email = self.request.get('email')
		password = self.request.get('password')
		verify = self.request.get('verify')

		valid_fname, fname_error = validate_username(fname)
		valid_lname, lname_error = validate_username(lname)
		valid_email, email_error = validate_email(email)
		valid_pass, pass_error = validate_password(password)
		valid_verify, verify_error = match_passwords(password, verify)

		if valid_fname and valid_lname and valid_email and valid_pass and valid_verify:
			verification_link = self.register_user(fname, lname, email, password)
			self.write('Link is: %s' % verification_link)
			# activation_mail(email = email, fname = fname, lname = lname, link = verification_link)
			# self.write('Verification link sent to the mail: %s' % email)	#TODO: mail activation and redirection

		else:
			if not valid_pass:
				verify_error = ''
			self.render_page(pane='signup',
							fname=fname,
							lname=lname,
							email=email,
							fname_error=fname_error,
							lname_error=lname_error,
							email_error=email_error,
							pass_error=pass_error,
							verify_error=verify_error)

	def register_user(self, fname, lname, email, password):
		candidate = Candidate(fname = fname, lname = lname, email = email, email_pw_salt = ' ')
		verification_link = candidate.store(password)
		return verification_link

	def signin(self):
		email = self.request.get('email')
		password = self.request.get('password')

		user_id = User.validate_email_pw(email, password)
		if user_id == None:
			login_error = 'Invalid email or password'
			self.render_page(pane='signin', email=email, login_error=login_error)
		else:
			self.set_cookie(user_id)		
			self.redirect('/dashboard/')	#TODO: redirect to the dashboard

class Activate(Handler):
	def get(self):
		link = self.request.get('link')
		forgot = self.request.get('forgot')
		success = self.request.get('success')
		if success:
			self.render('password_change.html',success = success)
		elif forgot:
			self.render('password_change.html',link = link)
		else:
			response = User.activate(link)
			if response is not None:
				self.write('Signup successful')
			else:
				self.error(404)
				self.render('error.html', error = 'Activation link expired or Invalid activation link')
	def post(self):
		link = self.request.get('link')
		user = User.get_by_activation_link(link)
		if user is None:
			self.redirect('/login?pane=signin')
		new_pass = self.request.get('new_pass')
		verify = self.request.get('verify')

		old_pass_actual = user.email_pw_salt
		email = user.email
		pos = old_pass_actual.find(DELIM)
		salt = old_pass_actual[pos+1:]

		valid_pass, pass_error = validate_password(new_pass)
		valid_verify, verify_error = match_passwords(new_pass, verify)

		if valid_pass and valid_verify:
			new_salt = hash_email_pw(email,new_pass,salt)
			user.email_pw_salt = new_salt
			user.put()
			message = "Password changed successfully"
			self.redirect('/activate?success=1')
			# verification_link = self.register_user(fname, lname, email, password)
			# self.write('Link is: %s' % verification_link)
			# activation_mail(email = email, fname = fname, lname = lname, link = verification_link)
			# self.write('Verification link sent to the mail: %s' % email)	#TODO: mail activation and redirection

		else:
			if not valid_pass:
				verify_error = ''

			self.render('password_change.html',
							pass_error=pass_error,
							verify_error=verify_error)


class LogoutPage(Handler):
	def get(self):
		self.set_cookie()
		self.redirect('/')

class CatalogPage(Handler):
	def get(self):
		self.render('catalog.html')

class HomePage(Handler):
	def get(self):
		self.render('home.html')


class ProfilePage(Handler):
	def get(self):
		# user = self.cookie_user()
		self.render('profile.html')

	def post(self):
		fname = self.request.get('fname')
		lname = self.request.get('lname')
		user = self.cookie_user()
		if fname:
			user.fname = fname
		if lname:
			user.lname = lname
		user.put()
		self.redirect('/profile/')
	
class ChangePassword(Handler):
	def render_form(self, **kw):
		self.render('password.html', **kw)

	def get(self):
		success = self.request.get('success')
		if success:
			self.render_form(success=success)
		else:
			self.render_form()

	def post(self):
		user = self.cookie_user()
		if user is None:
			self.redirect('/login?pane=signin')
		old_pass = self.request.get('old_pass')
		new_pass = self.request.get('new_pass')
		verify = self.request.get('verify')

		old_pass_actual = user.email_pw_salt
		email = user.email
		pos = old_pass_actual.find(DELIM)
		salt = old_pass_actual[pos+1:]

		# valid_fname, fname_error = validate_username(fname)
		# valid_lname, lname_error = validate_username(lname)
		valid_oldpass, oldpass_error = validate_oldpass(old_pass,user)
		valid_pass, pass_error = validate_password(new_pass)
		valid_verify, verify_error = match_passwords(new_pass, verify)

		if valid_oldpass and valid_pass and valid_verify:
			new_salt = hash_email_pw(email,new_pass,salt)
			user.email_pw_salt = new_salt
			user.put()
			message = "Password changed successfully"
			self.redirect('/profile/change-passwd?success=1')
			# verification_link = self.register_user(fname, lname, email, password)
			# self.write('Link is: %s' % verification_link)
			# activation_mail(email = email, fname = fname, lname = lname, link = verification_link)
			# self.write('Verification link sent to the mail: %s' % email)	#TODO: mail activation and redirection

		else:
			if not valid_oldpass:
				pass_error = ''
				verify_error = ''
			if not valid_pass:
				verify_error = ''

			self.render_form(oldpass_error=oldpass_error,
							pass_error=pass_error,
							verify_error=verify_error)


class ForgotPasswordPage(Handler):
	def get(self):
		self.render('forgot_password.html')
	def post(self):
		emailid = self.request.get('email')
		user = User.get_by_email(emailid)
		if user == None:
			login_error = 'Sorry! This Email ID does not exist.'
			self.render('forgot_password.html', email=emailid, email_error=login_error)
		else:
			verification_link = ''.join(['be-ingenious.appspot.com/activate?link=',user.email_pw_salt,'&forgot=1'])
			self.write('Link is: %s' % verification_link)
			# activation_mail(email = email, fname = fname, lname = lname, link = verification_link)
			# self.write('Verification link sent to the mail: %s' % email)	#TODO: mail activation and redirection




		


