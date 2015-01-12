from google.appengine.ext import ndb

class Configuration(ndb.Model):
	key = ndb.StringProperty()
	value = ndb.StringProperty()

class SeenUrl(ndb.Model):
	url = ndb.StringProperty(required=True)
	section = ndb.StringProperty(required=True)
	reported = ndb.BooleanProperty(default=False)
	seen = ndb.DateTimeProperty(auto_now_add=True)

class ScrapeJob(ndb.Model):
	edition = ndb.StringProperty(required=True, default='uk')
	max_entries = ndb.IntegerProperty(required=True, default=3)
	site = ndb.StringProperty(required=True)
	topic = ndb.StringProperty()
