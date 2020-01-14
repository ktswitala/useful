
class ObjectSupervisor(object):
	def __init__(self):
		self.obj_defns = {}
		self.objs = {}

		self.on_create_fns = {}

		self.attr_deps = {}
		self.fn_deps = collections.defaultdict(set)
		self.general_deps = {}

	def new_define(self, name, create, args=None, kwargs=None):
		defn = Object()
		defn.created = False
		defn.name = name
		defn.create = create
		defn.args = args
		defn.kwargs = kwargs
		if args is None:
			defn.args = []
		if kwargs is None:
			defn.kwargs = {}
		return defn

	def get(self, name):
		return self.objs[name]

	def on_create(self, name, fn):
		self.on_create_fns[name] = fn

	def define_obj(self, name, create, args=None, kwargs=None):
		self.obj_defns[name] = self.new_define(name, create, args=args, kwargs=kwargs)

	def define_attr_dep(self, dependent_name, attr_name, dependency_name):
		self.attr_deps[(dependent_name, attr_name)] = dependency_name

	def define_fn_dep(self, dependent_name, fn_name, dependency_name):
		self.fn_deps[(dependent_name, fn_name)].add(dependency_name)

	def define_general_dep(self, name, dependent_name, dependency_name, dep_fn):
		self.general_deps[(name, dependent_name, dependency_name)] = dep_fn

	def create_all(self):
		for name, defn in self.obj_defns.items():
			if name not in self.objs:
				self.objs[name] = defn.create(*defn.args, **defn.kwargs)
				if name in self.on_create_fns:
					self.on_create_fns[name](self.objs[name])

	def inject_all(self):
		for (dependent_name, attr_name), dependency_name in self.attr_deps.items():
			setattr(self.objs[dependent_name], attr_name, self.objs[dependency_name])
		for (dependent_name, fn_name), dependency_names in self.fn_deps.items():
			for dependency_name in dependency_names:
				getattr(self.objs[dependent_name], fn_name)(dependency_name, self.objs[dependency_name])
		for (name, dependent_name, dependency_name), fn in self.general_deps.items():
			obj1 = self.get(dependent_name)
			obj2 = self.get(dependency_name)
			fn(obj1, obj2)

class Namespace(object):
	def __init__(self, name):
		self.name = name

	def __getattr__(self, rest):
		return object.__getattribute__(self, 'name') + "." + rest

class FileState(object):
	def __init__(self, file_manager, path):
		self.file_manager = file_manager
		self.path = path

	def get(self):
		if os.path.exists(self.path):
			return dill.loads(self.file_manager.open_bytes(self.path))
		else:
			return None

	def set(self, state):
		self.file_manager.save_bytes( self.path, dill.dumps(state, byref=True) )

class ObjectManager(object):
	def __init__(self, create, get_state, set_state):
		self.create = create
		self.get_state = get_state
		self.set_state = set_state

	def load(self):
		state = self.get_state()
		if state is None:
			return self.create()
		else:
			return state

	def save(self, state):
		self.set_state(state)
