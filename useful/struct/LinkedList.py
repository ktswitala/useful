
class LinkedList(object):
	def __init__(self):
		self.start_node = None
		self.end_node = None

		self.get_next = None
		self.set_next = None

		self.get_prev = None
		self.set_prev = None

		self.current_iter_id = 0
		self.iters = {}

	def register_next_fn(self, g, s):
		self.get_next = g
		self.set_next = s

	def register_prev_fn(self, g, s):
		self.get_prev = g
		self.set_prev = s

	def is_empty(self):
		if self.start_node is None:
			return True
		else:
			return False

	def get_start_node(self):
		return self.start_node

	def get_end_node(self):
		return self.end_node

	def append(self, node):
		self.set_next(node, None)

		if self.start_node is None:
			self.start_node = node
			self.set_prev(node, None)

		if self.end_node is not None:
			self.set_next(self.end_node, node)

		self.set_prev(node, self.end_node)
		self.end_node = node

	def remove(self, node):
		prev_node = self.get_prev(node)
		next_node = self.get_next(node)

		if next_node is not None:
			self.set_prev(next_node, prev_node)
		if prev_node is not None:
			self.set_next(prev_node, next_node)

		if self.start_node is node:
			self.start_node = next_node

		if self.end_node is node:
			self.end_node = prev_node

		update_itr = []
		for itr in self.iters.values():
			if itr is node:
				update_itr.append( (itr, self.get_next(node)))
		self.iters.update(update_itr)

	def iter(self):
		iter_id = self.current_iter_id
		self.current_iter_id += 1

		self.iters[iter_id] = self.start_node

		return LinkedListIter(self, iter_id)

	def iter_reset(self, iter_id):
		self.iters[iter_id] = self.start_node

	def iter_next(self, iter_id):
		if iter_id not in self.iters:
			return None
		node = self.iters[iter_id]
		if node is not None:
			self.iters[iter_id] = self.get_next(node)
		return node

class LinkedListIter(object):
	def __init__(self, ll, iter_id):
		self.ll = ll
		self.iter_id = iter_id

	def __iter__(self):
		return self

	def __next__(self):
		node = self.ll.iter_next(self.iter_id)
		if node:
			return node
		else:
			raise StopIteration
