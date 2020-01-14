
class BFSTraveler(object):
	events = ['tree_finished', 'node_started', 'node_finished', 'visit_edge']

	def __init__(self):
		self.get_iter = RaiseNotImplementedFn
		for event in BFSTraveler.events:
			setattr(self, event, PassNotImplementedFn)

	def begin(self, state):
		node = {"state":state, "iter":self.get_iter(state)}
		q = collections.deque()
		q.append(node)
		return q

	def travel(self, q):
		if len(q) == 0:
			self.tree_finished()
			return q

		hi_node = q[0]

		finished = False
		try:
			state = next(hi_node["iter"])
			lo_node = {}
			lo_node["state"] = state
			lo_node["iter"] = self.get_iter(state)
			self.node_started(lo_node["state"])
		except StopIteration:
			finished = True
			q.popleft()
			self.node_finished(hi_node["state"])

		if not finished:
			q.append( lo_node )
			self.visit_edge(hi_node["state"], lo_node["state"])

		return q
