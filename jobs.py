import webapp2
import json
import logging
from urllib import quote, urlencode
from google.appengine.api import urlfetch

import headers
import feed_reader

class GoogleNewsScrape(webapp2.RequestHandler):
	def get(self, edition):

		data = {
			'edition': edition,
			'links': feed_reader.read_edition(edition),
		}

		headers.json(self.response)

		self.response.out.write(json.dumps(data))

app = webapp2.WSGIApplication([('/jobs/edition/(\w+)', GoogleNewsScrape)],
                              debug=True)