import webapp2
import json
import logging
import datetime

from urllib import quote, urlencode
from urlparse import urlparse

from google.appengine.api import urlfetch
from google.appengine.api import mail

import headers
import feed_reader
import models
import configuration
import gae
import content_api

def today():
	return datetime.date.today().isoformat()

def read_headline(link_url):
	parsed_url = urlparse(link_url)

	if 'www.theguardian.com' in parsed_url.hostname:
		data = content_api.read(parsed_url.path, {'show-fields': 'headline'})
		if not data:
			return None

		json_data = json.loads(data)

		if 'response' in json_data:
			if 'content' in json_data['response']:
				if 'fields' in json_data['response']['content']:
					if 'headline' in json_data['response']['content']['fields']:
						return json_data['response']['content']['fields']['headline']

		return None


class GoogleNewsScrape(webapp2.RequestHandler):
	def get(self, edition=None):

		editions = []
		data = []

		if not edition:
			editions = ['uk', 'us', 'au']

		for current_edition in editions:

			seen_links = feed_reader.read_edition(current_edition)

			new_links = []

			for link_url in seen_links:
				link_record = models.SeenUrl.query(models.SeenUrl.url == link_url).fetch()

				if not link_record:
					new_link_record = models.SeenUrl(url=link_url, section=current_edition)

					headline = read_headline(link_url)

					if headline:
						new_link_record.headline = headline

					new_link_record.put()
					new_links.append(link_url)

			data.append({
				'edition': current_edition,
				'seen_links': new_links,
			})

		headers.json(self.response)

		self.response.out.write(json.dumps(data))

class PostReporter(webapp2.RequestHandler):
	def get(self):
		headers.text(self.response)

		new_urls_query = models.SeenUrl.query(models.SeenUrl.reported == False)

		new_urls = {}

		for newly_seen in new_urls_query:
			if newly_seen.section in new_urls:
				new_urls[newly_seen.section].append(newly_seen)
			else:
				new_urls[newly_seen.section] = [newly_seen]

			if not gae.is_development():
				newly_seen.reported = True
				newly_seen.put()

		if not new_urls:
			self.response.out.write("No new urls seen")
			return

		sender_address = configuration.lookup('SENDER_EMAIL')
		recipients = configuration.lookup('GNEWS_ALERT_EMAILS', '').split(",")

		subject = 'New Guardian stories spotted on Google News: {0}'.format(today())

		body = ""

		for section, urls in new_urls.items():

			body = body + "Section: {0}\n\n".format(section)
			for url in urls:
				parsed_url = urlparse(url.url)

				if url.headline:
					body = body + "{0}\n".format(url.headline)

				body = body + "{0}\n".format(url.url)
				body = body + "Ophan: https://dashboard.ophan.co.uk/info?path={0}&referrer=google\n".format(parsed_url.path)
				body = body + '\n'

			body = body + "\n"

		if sender_address:
			mail.send_mail(sender_address, recipients, subject, body)

		self.response.out.write(body)

app = webapp2.WSGIApplication([
	('/jobs/scrape', GoogleNewsScrape),
	('/jobs/edition/(\w+)', GoogleNewsScrape),
	('/jobs/report', PostReporter),],
                              debug=True)