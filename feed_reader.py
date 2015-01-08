import feedparser

from urlparse import urlparse, parse_qs


google_news_url='http://news.google.com/news?ned={edition}&hl=en&output=atom&num={total}'

d = feedparser.parse(google_news_url)

def extract_link(google_news_url):
	return parse_qs(urlparse(google_news_url).query).get('url', [])[0]

guardian_urls = [extract_link(e.link) for e in d.entries if 'theguardian.com' in e.link]

def read_edition(edition, site_name='theguardian.com', max_entries=6):
	edition_url = google_news_url.format(edition=edition, total=max_entries)
	feed_data = feedparser.parse(edition_url)
	return [extract_link(e.link) for e in feed_data.entries if site_name in e.link]