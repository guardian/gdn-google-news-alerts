from urlparse import urlparse, parse_qs


google_news_url='http://news.google.com/news?ned=us&hl=en&output=rss&num=30'

d = feedparser.parse(google_news_url)

def extract_link(google_news_url):
	return parse_qs(urlparse(google_news_url).query).get('url', [])[0]

guardian_urls = [extract_link(e.link) for e in d.entries if 'theguardian.com' in e.link]