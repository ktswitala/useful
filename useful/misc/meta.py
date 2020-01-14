
def create_getset(name):
	def get_attr(obj):
		return getattr(obj, name)
	def set_attr(obj1, obj2):
		setattr(obj1, name, obj2)
		
	return (get_attr, set_attr)
