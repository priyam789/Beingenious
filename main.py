import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'scripts'))

from login import *
from activities import *
from dashboard import *
from add_course import *
from course_page import *

app = webapp2.WSGIApplication([
	('/', HomePage),
	('/catalog/?', CatalogPage),
	('/login', LoginPage),
	('/activate', Activate),
	('/logout/?', LogoutPage),
	('/activities/?', ActivityPage),
	('/dashboard/?', DashboardPage),
	('/profile/?', ProfilePage),
	('/create_course/?',Add_course),
	('/courses/?', CoursePage)
	], debug = True)