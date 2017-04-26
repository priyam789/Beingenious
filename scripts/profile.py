from base import *

class ProfilePage(Handler):
	def get(self):
		self.render('profile.html')
		
