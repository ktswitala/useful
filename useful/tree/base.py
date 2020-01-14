
tree_events = ['tree_finished', 'node_started', 'node_finished', 'visit_edge']

def get_branch(start_branch, path, get_branch):
	rval = None
	def final_visit(final_branch):
		nonlocal rval
		rval = final_branch
	visit_path(start_branch, path, get_branch, final_visit=final_visit)
	return rval
