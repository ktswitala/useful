
class CartesianIter(object):
	def __init__(self, sizes):
		self.sizes = list(sizes)
		self.indices = len(self.sizes)*[0]
		self.finished = False

	def inc(self, index):
		if index == len(self.sizes):
			self.finished = True
			return
		value = self.indices[index]
		if value == self.sizes[index]:
			self.indices[index] = 0
			self.inc(index+1)
		else:
			self.indices[index] += 1

	def next(self):
		indices = list(self.indices)
		self.inc(0)
		return indices

class ListIterator(object):
	def __init__(self, l, pos=0):
		self.l = l
		self.pos = pos

	def __next__(self):
		if self.pos >= len(self.l):
			raise StopIteration()
		val = self.get()
		self.pos += 1
		return val

	def get(self):
		return self.l[self.pos]

	def save(self):
		return (l, pos)

	def restore(state):
		return ListIterator(state[0],pos=state[1])
