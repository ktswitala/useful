
import pymongo
import os, codecs

class MongoKVStore(object):
	def __init__(self, c, index=True):
		self.c = c
		self.index = index
		if index:
			self.c.create_index([('key', pymongo.ASCENDING)], unique=True)

	def exists(self, key):
		return self.read(key) is not None

	def create(self, key, value):
		self.c.update_one({'key':key, 'value':value}, {'$set': {'key':key, 'value':value}})

	def read(self, key):
		item = self.c.find_one({'key':key})
		if item is not None:
			return item["value"]
		else:
			return None

	def update(self, key, value, upsert=False):
		self.c.update_one({'key':key, 'value':value}, {'$set': {'key':key, 'value':value}}, upsert=upsert)

	def delete(self, key):
		self.c.delete_one({'key':key})

class DirectoryKVStore(object):
	class Exception(Exception):
		pass

	def __init__(self, source_directory):
		self.source_directory = source_directory
		self.encoding = "utf-8"

	def exists(self, key):
		filename = os.path.join(self.source_directory, key)
		return os.path.exists(filename)

	def create(self, key, value):
		filename = os.path.join(self.source_directory, key)
		if self.exists(key):
			raise Exception(DirectoryKVStore, "create on existing key")
		f = codecs.open(filename, "w", encoding=self.encoding)
		f.write(value)
		f.close()

	def read(self, key):
		filename = os.path.join(self.source_directory, key)
		try:
			f = codecs.open(filename, "r", encoding=self.encoding)
			value = f.read()
			f.close()
			return value
		except:
			return None

	def update(self, key, value, upsert=False):
		filename = os.path.join(self.source_directory, key)
		if not self.exists(key) and not upsert:
			raise Exception(DirectoryKVStore, "update on non-existing key")
		f = codecs.open(filename, "w", encoding=self.encoding)
		f.write(value)
		f.close()

	def delete(self, key):
		filename = os.path.join(self.source_directory, key)
		os.remove(filename)

class KVTransaction(object):
	def __init__(self, store, key, value):
		self.store = store
		self.key = key
		self.new_value = values

	def apply(self, key, value):
		self.old_value = self.store.read(key)
		self.store.update(self.key, self.new_value, upsert=True)

	def rollback(self):
		if hasattr(self, 'old_value'):
			self.store.update(self.key, self.old_value, upsert=True)
