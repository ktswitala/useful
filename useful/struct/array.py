
import collections

def expect_1(a):
	if len(a) == 1:
		return a[0]
	else:
		return None

def argmin(a):
	min = None
	min_i = None
	for i, e in enumerate(a):
		if min is None:
			min = e
			min_i = i
		if e < min:
			min = e
			min_i = i
	return min_i

class Chunker(object):
	def __init__(self, chunk_size, sparsity=0):
		self.chunk_size = chunk_size
		self.sparsity = sparsity
		self.position = 0

	def next(self):
		chunk = (self.position, chunk_size)
		self.position += self.chunk_size
		self.position += self.sparsity
		return chunk
