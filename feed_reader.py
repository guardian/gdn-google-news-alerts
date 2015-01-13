import feedparser

from urlparse import urlparse, parse_qs


google_news_url='http://news.google.com/news?ned={edition}&hl=en&output=atom&num={total}'

d = feedparser.parse(google_news_url)

def extract_link(google_news_url):
	return parse_qs(urlparse(google_news_url).query).get('url', [])[0]

guardian_urls = [extract_link(e.link) for e in d.entries if 'theguardian.com' in e.link]

def create_rss_url(edition, topic, max_entries):
	url = google_news_url.format(edition=edition, total=max_entries)

	if topic:
		url = url + "&topic={0}".format(topic)

	return url

def read_edition(edition, site_name='www.theguardian.com', max_entries=30, topic=None):
	rss_url = create_rss_url(edition, topic, max_entries)
	feed_data = feedparser.parse(rss_url)
	return [extract_link(e.link) for e in feed_data.entries if site_name in e.link]