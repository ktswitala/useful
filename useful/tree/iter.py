
def dfs_iter_depth(traveler, visit_fn):
	depth = 0
	def node_started(state):
		depth += 1
		visit_fn(depth, state)
	def node_finished(state):
		depth -= 1

	traveler.node_started = compose(traveler.node_started, node_started)
	traveler.node_finished = compose(traveler.node_finished, node_finished)
	return traveler

def iter_max_depth(traveler, max_depth=None):
	get_iter_orig = traveler.get_iter
	depths = {}
	def tree_started(root):
		depths[id(root)] = 0
	def get_iter(state):
		depth = depths[id(state)]
		if depth < max_depth:
			for substate in get_iter_orig(state):
				depths[id(substate)] = depth + 1
				yield substate
	traveler.tree_started = compose(traveler.tree_started, tree_started)
	traveler.get_iter = get_iter
	return traveler

def exhaust_traveler(traveler, start_state):
	state = traveler.begin(start_state)
	while state != []:
		state = traveler.travel(state)

def apply(traveler, start_branch, visit_fn):
	def apply_visit(branch):
		visit_fn(branch)

	traveler.node_started = compose(traveler.node_started, apply_visit)

	state = traveler.begin(start_branch)
	while state != []:
		state = traveler.travel(state)

def transform(traveler,transform_fn,link_fn):
	nodes = {}
	root = None

	old_node_started = traveler.node_started
	old_visit_edge = traveler.visit_edge
	old_tree_started = traveler.tree_started

	def get_root():
		return root

	def tree_started(state):
		old_tree_started(state)

		nonlocal root
		root = nodes[id(state)]

	def node_started(state):
		old_node_started(state)

		tsm_state = transform_fn(state)
		nodes[id(state)] = tsm_state
	def visit_edge(hi_state, lo_state):
		old_visit_edge(hi_state, lo_state)

		tsm_hi_state = nodes[id(hi_state)]
		tsm_lo_state = nodes[id(lo_state)]
		link_fn(tsm_hi_state, tsm_lo_state)

	traveler.node_started = node_started
	traveler.visit_edge = visit_edge
	traveler.tree_started = tree_started
	return traveler, get_root

def all(traveler, stack):
	l = []
	def visit(hi_node, lo_node):
		l.append(lo_node)

	traveler.visit_edge = visit
	while traveler.travel(stack):
		pass

	return l

def visit_path(start_branch, path, get_branch, visit=None, final_visit=None):
	current_branch = start_branch
	while True:
		try:
			segment = next(path)
			if visit is not None:
				visit(current_branch)
			current_branch = get_branch(current_branch, segment)
		except StopIteration:
			if final_visit is not None:
				final_visit(current_branch)
			return
