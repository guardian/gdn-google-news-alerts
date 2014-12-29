from google.appengine.ext import ndb

class Configuration(ndb.Model):
	key = ndb.StringProperty()
	value = ndb.StringProperty()

class SeenUrl(ndb.Model):
	url = ndb.StringProperty(required=True)
	section = ndb.StringProperty(required=True)
	reported = ndb.BooleanProperty(default=False)
	seen = ndb.DateTimeProperty(auto_now_add=True)