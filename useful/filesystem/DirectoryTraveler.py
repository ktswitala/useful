
class DirectoryTraveler(object):
	def __init__(self, traveler):
		self.traveler = traveler()
		self.traveler.get_iter = self.get_iter
		self.traveler.visit_edge = self.visit_edge

		self.state = None
		self.finished = False

	def begin(self, path):
		self.state = self.traveler.begin(path)
		self.finished = False
		self.seek_next()

	def seek_next(self):
		self.visited = False
		while self.visited is False and self.finished is False:
			self.state = self.traveler.travel(self.state)
			if len(self.state) == 0:
				self.finished = True

	def next(self):
		next_path = self.current_path
		self.seek_next()
		return next_path

	def visit_edge(self, node_hi, node_lo):
		self.visited = True
		self.current_path = node_lo

	def get_iter(self, base_path):
		if os.path.isdir(base_path):
			itr = ListIterator([os.path.join(base_path, path) for path in os.listdir(base_path)])
			return itr
		else:
			return ListIterator([])

	def save(self):
		state = list(map(lambda li: li.save(), self.state))
		finished = self.finished
		def restore(traveler):
			dt = DirectoryTraveler(traveler)
			dt.state = list(map(lambda li: li(), state))
			dt.finished = finished
			return dt
