
class History(object):
	def __init__(self, n, add, remove, update):
		self.dq = collections.deque()
		self.ready = False

		self.n = n
		self.add = add
		self.remove = remove
		self.update = update

	def append(self, value):
		self.dq.append(value)
		self.add(value)
		if len(self.dq) == self.n+1:
			old_value = self.dq.popleft()
			self.remove(old_value)
			self.ready = True
		elif len(self.dq) <= self.n:
			pass
		else:
			raise Exception("queue mis-sized")
		self.update()

	def len(self):
		return len(self.dq)

	def all(self):
		for e in self.dq:
			yield e
