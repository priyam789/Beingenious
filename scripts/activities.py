import re
from datetime import date
from base import *
class ActivityPage(Handler):	#TODO: will go in a separate file
	def get(self):
		category = self.request.get('category')
		
		category_list = Course.get_category_events(category)
		# self.write(category)
		self.render('activity.html',category = category,categ_list = category_list)