import webapp2
import json
import logging
from urllib import quote, urlencode

from google.appengine.api import urlfetch
from google.appengine.api import mail

import headers
import feed_reader
import models
import configuration

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

class PostReporter(webapp2.RequestHandler):
	def get(self):
		headers.text(self.response)

		new_urls_query = models.SeenUrl.query(models.SeenUrl.reported == False)

		new_urls = {}

		for newly_seen in new_urls_query:
			if newly_seen.section in new_urls:
				new_urls[newly_seen.section].append(newly_seen.url)
			else:
				new_urls[newly_seen.section] = [newly_seen.url]

			newly_seen.reported = True
			newly_seen.put()

		if not new_urls:
			self.response.out.write("No new urls seen")
			return

		sender_address = configuration.lookup('SENDER_EMAIL')
		recipients = configuration.lookup('GNEWS_ALERT_EMAILS').split(",")

		subject = 'New Guardian stories spotted on Google News'

		body = ""

		for section, urls in new_urls.items():
			body = body + "Section: {0}\n\n".format(section)
			for url in urls:
				body = body + "{0}\n".format(url)

			body = body + "\n"

		mail.send_mail(sender_address, recipients, subject, body)

		self.response.out.write(body)

app = webapp2.WSGIApplication([
	('/jobs/edition/(\w+)', GoogleNewsScrape),
	('/jobs/report', PostReporter),],
                              debug=True)