
class WriteBuffer(object):
	def __init__(self, size):
		self.updates = []
		self.size = size

	def ready(self):
		return len(self.updates) >= self.size

	def flush(self, c):
		if len(self.updates) == 0:
			return
		c.bulk_write(self.updates)
		self.updates = []

	def append(self, update):
		self.updates.append(update)

# unfinished
class SetQueryBuffer(object):
	def __init__(self, values, query):
		self.buffered_results = []
		self.values = values
		self.query = query

	def fill_buffer(self):
		values = []
		try:
			for i in range(0,1000):
				values.append(self.values.pop())
		except IndexError:
			pass
		if len(values) == 0:
			self.buffered_results = []
		else:
			self.buffered_results = self.query(values)

	def next(self):
		if len(self.buffered_results) == 0:
			self.fill_buffer()
		if len(self.buffered_results) == 0:
			raise StopIteration
		yield

class MongoAgg(object):
	def min(agg, field):
		docs = agg.sort({field:1}).limit(1).execute()
		try:
			return docs.next()[field]
		except StopIteration:
			return None

	def max(agg, field):
		docs = agg.sort({field:-1}).limit(1).execute()
		try:
			return docs.next()[field]
		except StopIteration:
			return None

	def to_dict(agg, field):
		return {doc[field]:doc for doc in agg.execute()}

	def exists(agg, field, values):
		returned_values = [doc[field] for doc in agg.exists_in(field, values).project(includes=[field]).execute()]
		exists_dict = {}
		for value in values:
			if value in returned_values:
				exists_dict[value] = True
			else:
				exists_dict[value] = False
		return exists_dict

class MongoCollection(object):
	def __init__(self, c, uuid_field):
		self.c = c
		self.uuid_field = uuid_field

	def query(self):
		return AggregateBuilder(self.c)

	def find_one(self, agg):
		docs = agg.limit(1).execute()
		try:
			return docs.next()
		except StopIteration:
			return None

	def bulk_write(self, writes):
		if len(writes) == 0:
			return
		try:
			self.c.bulk_write(writes)
		except pymongo.errors.BulkWriteError as bwe:
			from pprint import pprint
			pprint(bwe.details)
			raise

	def replace_one(self, doc):
		return pymongo.ReplaceOne({self.uuid_field:doc[self.uuid_field]}, doc, upsert=True)

	def insert_one(self, doc):
		return pymongo.InsertOne(doc)

	def delete_one(self, uuid):
		return pymongo.DeleteOne({self.uuid_field:uuid})

	def update(self, expr):
		uuid = doc[self.uuid_field]
		return pymongo.UpdateOne({self.uuid_field:uuid}, expr, upsert=True)

	def group_command(self, command, docs):
		ops = []
		for doc in docs:
			ops.append( command(doc) )
		if len(ops) == 0:
			return None
		return self.c.bulk_write(ops)
