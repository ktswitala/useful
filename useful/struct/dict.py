
def filter_dict_values(fn, d):
	new_d = {}
	for k, v in d.items():
		if fn(v) is True:
			new_d[k] = v
	return new_d

def order_keys(d):
	key_order = list(d.keys())
	key_order.sort()
	return key_order
