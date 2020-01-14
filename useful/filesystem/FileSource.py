
class SeekFlag(object):
	BEGIN = 0
	CURRENT = 1
	END = 2

class FileSource(object):
	def __init__(self, f):
		self.f = f
		self._finished = False

	def position(self):
		return self.f.tell()

	def seek(self, position, flag=0):
		return self.f.seek(position, flag)

	def read(self, amt):
		data = self.f.read(amt)
		if len(data) == 0:
			self._finished = True
		return data

	def finished(self):
		return self._finished
