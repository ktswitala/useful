
def dupdate_obj(obj, d, keys=None):
	if keys is None:
		keys = d.keys()
	for key in keys:
		setattr(obj, key, d[key])

def dslice_obj(obj, attrs):
	result = {}
	for attr in attrs:
		result[attr] = getattr(obj,attr)
	return result

class Object(object):
	def __init__(self, **kwargs):
		for key, value in kwargs.items():
			setattr(self, key, value)

	@staticmethod
	def from_obj(obj, attrs):
		o = useful.Object()
		for attr in attrs:
			setattr(o, attr, getattr(obj, attr, None))
		return o

	def __repr__(self):
		return "OBJECT({})".format(str(self.__dict__))
