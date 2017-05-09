import re
from datetime import date
from base import *
# This class handles the display of the list of activities in the catalog
class ActivityPage(Handler):	
	def get(self):
		category = self.request.get('category')
		
		category_list = Course.get_category_events(category)
		# self.write(category)
		self.render('activity.html',category = category,categ_list = category_list)