
class FileManager(object):
	class Exception(Exception):
		pass

	def __init__(self, throw_on_nonexist=False, encoding='utf-8'):
		self.throw_on_nonexist = throw_on_nonexist
		self.encoding = encoding

	def open(self, filename, default=None):
		if os.path.exists(filename):
			f = codecs.open(filename, "r", encoding=self.encoding)
			data = f.read()
			f.close()
			if len(data) == 0:
				return default
			return data
		else:
			if self.throw_on_nonexist:
				raise FileData.Exception("file doesnt exist")
			return default

	def open_bytes(self, filename):
		f = open(filename, "rb")
		data = f.read()
		f.close()
		return data

	def save_bytes(self, filename, data):
		f = open(filename, "wb")
		f.write( data )
		f.close()

	def save(self, filename, data):
		f = codecs.open(filename, "w", encoding=self.encoding)
		f.write( data )
		f.close()
