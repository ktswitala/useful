
class TreeLinker(object):
	def __init__(self):
		self.links = {}
		self.nodes = {}
		self.get_key = RaiseNotImplementedFn

	def set_root(self, node):
		key = self.get_key(node)
		self.nodes[key] = node
		self.links[key] = []

	def add_edge(self, node_hi, node_lo):
		key_hi = self.get_key(node_hi)
		key_lo = self.get_key(node_lo)

		if key_hi not in self.links:
			raise Exception("cannot add unrooted state")
		if key_lo in self.nodes:
			raise Exception("cannot add multiple links to child node")
		if key_lo not in self.links:
			self.links[key_lo] = []

		self.links[key_hi].append(node_lo)
		self.nodes[key_lo] = node_lo

	def get_links(self, node):
		key = self.get_key(node)
		return self.links[key]
