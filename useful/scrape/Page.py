
import uuid
import urllib.parse
import bs4

class Page(object):
	def __init__(self, url, source):
		self.url = url
		self.source =  source
		self.parsed_url = urllib.parse.urlparse(url)

	@useful.lazyprop
	def soup(self):
		return bs4.BeautifulSoup(self.source, 'html.parser')
