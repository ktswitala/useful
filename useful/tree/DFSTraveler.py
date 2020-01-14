
class DFSTraveler(object):
	events = ['tree_finished', 'tree_started', 'node_started', 'node_finished', 'visit_edge']

	def __init__(self):
		self.get_iter = RaiseNotImplementedFn
		for event in DFSTraveler.events:
			setattr(self, event, PassNotImplementedFn)

	def begin(self, state):
		node = {"state":state, "iter":self.get_iter(state)}
		self.node_started(state)
		self.tree_started(state)
		return [node]

	def travel(self, stack):
		if len(stack) == 0:
			self.tree_finished()
			return stack

		hi_node = stack[-1]

		finished = False
		try:
			state = next(hi_node["iter"])
			lo_node = {}
			lo_node["state"] = state
			lo_node["iter"] = self.get_iter(state)
			self.node_started(lo_node["state"])
		except StopIteration:
			finished = True
			stack.pop()
			self.node_finished(hi_node["state"])

		if not finished:
			stack.append(lo_node)
			self.visit_edge(hi_node["state"], lo_node["state"])

		return stack
