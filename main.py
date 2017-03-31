import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'scripts'))

from login import *

app = webapp2.WSGIApplication([
	('/', HomePage),
	('/catalog/?', CatalogPage),
	('/login', LoginPage),
	('/activities/?', ActivityPage)
	], debug = True)