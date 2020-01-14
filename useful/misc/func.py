
def apply_or_none(value, fn):
	if value is None:
		return None
	else:
		return fn(value)

def optional(fn):
	try:
		result = fn()
		return (result, None)
	except Exception as e:
		return (None, e)

def compose(*fns):
	def composed_fn(*args, **kwargs):
		for fn in fns:
			fn(*args, **kwargs)
	return composed_fn
