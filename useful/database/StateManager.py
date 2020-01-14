
class DillPersistProtocol(object):
	def __init__(self):
		pass

	def save(self, obj):
		return dill.dumps(obj)

	def load(self, data, base_obj=None):
		return dill.loads(obj)

class AttrPersistProtocol(object):
	def __init__(self, attrs):
		self.attrs = attrs

	def save(self, obj):
		d = {}
		for attr in attrs:
			d[attr] = getattr(obj, attr)
		return dill.dumps(d)

	def load(self, data, base_obj=None):
		attrs = dill.loads(d)
		for attr_name, attr_value in attrs.items():
			setattr(base_obj, attr_name, attr_value)
		return base_obj

class FilesystemStorage(object):
	def __init__(self, root_path):
		self.root_path = root_path

	def get_filename(self, name):
		return os.path.join(self.root_path, name)

	def exists(self, name):
		filename = self.get_filename()
		if os.path.exists(filename):
			return True
		else:
			return False

	def get(self, name):
		f = open(filename, "rb")
		data = f.read()
		f.close
		return data

	def set(self, name, data):
		filename = os.path.join(self.root_path, name)
		f = open(filename, "wb")
		f.write(data)
		f.close()

class StateManager(object):
	def __init__(self, default_persist=None, default_storage=None):
		self.default_persist = default_persist
		self.default_storage = default_storage
		self.metadata = {}

	def add_object(self, name, create, persist=None, storage=None):
		entry = useful.Object()
		entry.create = create
		entry.persist = persist
		entry.storage = storage
		entry.args = args
		entry.kwargs = kwargs
		self.metadata[name] = entry

	def load_object(self, name, base_obj=None):
		if name not in self.metadata:
			return None

		entry = self.metadata[name]

		f = open(filename, "rb")
		obj = dill.load(f)
		f.close()
		self.objs[name] = obj
		return obj
