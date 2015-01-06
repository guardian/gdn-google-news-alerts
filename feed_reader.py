import feedparser

from urlparse import urlparse, parse_qs


google_news_url='http://news.google.com/news?ned={edition}&hl=en&output=rss&num={total}'

d = feedparser.parse(google_news_url)

def extract_link(google_news_url):
	return parse_qs(urlparse(google_news_url).query).get('url', [])[0]

guardian_urls = [extract_link(e.link) for e in d.entries if 'theguardian.com' in e.link]

def read_edition(edition):
	edition_url = google_news_url.format(edition=edition, total=6)
	feed_data = feedparser.parse(edition_url)
	return [extract_link(e.link) for e in feed_data.entries if 'theguardian.com' in e.link]