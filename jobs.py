import webapp2
import json
import logging
from urllib import quote, urlencode
from google.appengine.api import urlfetch

import headers
import feed_reader
import models

class GoogleNewsScrape(webapp2.RequestHandler):
	def get(self, edition):

		seen_links = feed_reader.read_edition(edition)

		new_links = []

		for link_url in seen_links:
			link_record = models.SeenUrl.query(models.SeenUrl.url == link_url).fetch()

			if not link_record:
				new_link_record = models.SeenUrl(url=link_url, section=edition)
				new_link_record.put()
				new_links.append(link_url)

		data = {
			'edition': edition,
			'seen_links': new_links,
		}

		headers.json(self.response)

		self.response.out.write(json.dumps(data))

app = webapp2.WSGIApplication([('/jobs/edition/(\w+)', GoogleNewsScrape)],
                              debug=True)