

class Source(object):
	@staticmethod
	def read_fileobj(read_fn):
		def new_read(amt):
			data = read_fn(amt)
			if data == b"":
				return None
			else:
				return data
		return new_read

	@staticmethod
	def seek_fileobj(seek_fn):
		def new_seek(pos):
			return seek_fn(pos, 0)
		return new_seek

	def __init__(self):
		self._read = None
		self.time_control = useful.FlowRateControl()
		self.read_time = 0.1

	def seek(self, position):
		self._seek(position)

	def read(self):
		read_amount = self.time_control.amount_needed(self.read_time)
		if read_amount is None:
			read_amount = 1024*1024
		read_amount = int(read_amount)

		start_time = time.time()
		data = self._read(read_amount)
		if data is None:
			self.finished = True
			return None

		time_taken = time.time()-start_time
		#print(read_amount, time_taken)
		self.time_control.update(amount=read_amount, time=time_taken)

		return data
