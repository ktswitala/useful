
class AggregateBuilder(object):
	def __init__(self, c):
		self.pipeline = []
		self.c = c

	def execute(self):
		return self.c.aggregate(self.pipeline)

	def one(self):
		agg = self.c.aggregate(self.pipeline)
		try:
			v = agg.next()
		except StopIteration:
			v = None
		return v

	def __iadd__(self, pipeline):
		self.pipeline += pipeline
		return self

	def check_field_null(self, field, b):
		if b is True:
			self.match({field:{'$eq':None}})
		elif b is False:
			self.match({field:{'$ne':None}})
		else:
			raise Exception("expected boolean")

	def match(self, q):
		self.pipeline += [{'$match':q}]
		return self

	def match_group(self, field, group):
		self.pipeline += [{'$match':{field:{'$in':group}}}]
		return self

	def count(self):
		self.pipeline += [{'$count':'count'}]
		return self

	def limit(self, n):
		self.pipeline += [{'$limit':n}]
		return self

	def sample(self, n):
		self.pipeline += [{'$sample':{'size':n}}]
		return self

	def sort(self, fields):
		self.pipeline += [{'$sort':fields}]
		return self

	def project(self, includes=[], excludes=[]):
		projects = {}
		for include in includes:
			projects[include] = 1
		for exclude in excludes:
			projects[exclude] = 0
		self.pipeline += [{'$project':projects}]
		return self

	def sortByCount(self, expr):
		self.pipeline += [{'$sortByCount':expr}]
		return self
