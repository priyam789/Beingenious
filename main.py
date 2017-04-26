import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'scripts'))

from login import *
from profile import *
from activities import *
from dashboard import *
from add_course import *
from course_page import *
from edit_course import *
from video import *

app = webapp2.WSGIApplication([
	('/', HomePage),
	('/catalog/?', CatalogPage),
	('/login', LoginPage),
	('/activate', Activate),
	('/logout/?', LogoutPage),
	('/activities/?', ActivityPage),
	('/dashboard/?', DashboardPage),
	# ('/profile/change-passwd/?', ChangePassword),
	# ('/profile/?', ProfilePage),
	('/create_course/?',AddCourse),
	('/courses/(\w+)/?', CourseMainPage),
	('/courses/?', CoursePage),
	('/editcourse/(\w+)/?', EditCourse),
	('/view_video/(.*)', ServeVideo)
	], debug = True)