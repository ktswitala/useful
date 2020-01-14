

class RedisWrapper(object):
	def save_json(v):
		if v is not None:
			return simplejson.dumps(v)
		else:
			return None
	def load_json(b):
		if b is not None:
			return simplejson.loads(b.decode('utf-8'))
		else:
			return None
	def save_dill(v):
		if v is not None:
			return dill.dumps(v, byref=True)
		else:
			return None
	def load_dill(b):
		if b is not None:
			return dill.loads(b)
		else:
			return None
	def save_ascii(v):
		if v is not None:
			return v.encode('ascii')
		else:
			return None
	def load_ascii(b):
		if b is not None:
			return b.decode('ascii')
		else:
			return None
	def save_utf8(v):
		if v is not None:
			return v.encode('utf-8')
		else:
			return None
	def load_utf8(b):
		if b is not None:
			return b.decode('utf-8')
		else:
			return None

	def __init__(self, redis):
		self.redis = redis
		self.ascii = useful.RedisCoder(self.redis, encoder=RedisWrapper.save_ascii, decoder=RedisWrapper.load_ascii)
		self.json = useful.RedisCoder(self.redis, encoder=RedisWrapper.save_json, decoder=RedisWrapper.load_json)
		self.dill = useful.RedisCoder(self.redis, encoder=RedisWrapper.save_dill, decoder=RedisWrapper.load_dill)
		self.utf8 = useful.RedisCoder(self.redis, encoder=RedisWrapper.save_utf8, decoder=Redisrapper.load_utf8)

class RedisCoder(object):
	def __init__(self, redis, encoder=None, decoder=None):
		self.redis = redis
		self.encoder = encoder
		self.decoder = decoder

	def get(self, key, default=None):
		v = self.redis.get(key)
		if v is None:
			return default()
		else:
			return self.decoder(v)

	def set(self, key, value):
		return self.redis.set(key, self.encoder(value))

	def delete(self, *keys):
		return self.redis.delete(*keys)

	def pop(self, key, timeout=0, block=False):
		if block is True:
			value = self.redis.brpop(key, timeout)
		else:
			value = self.redis.rpop(key)
		return self.decoder(value)

	def hget(self, hkey, key):
		value = self.redis.hget(hkey, key)
		value = self.decoder(value)
		return value

	def hmget(self, hkey, keys):
		if len(keys) == 0:
			return {}
		d = dict(zip(keys, self.redis.hmget(hkey, keys)))
		for k, v in d.items():
			d[k] = self.decoder(v)
		return d

	def hgetall(self, hkey):
		d = self.redis.hgetall(hkey)
		for k, v in d.items():
			d[k] = self.decoder(v)
		return d

	def hset(self, hkey, key, value):
		return self.redis.hset(hkey, key, self.encoder(value))

	def hmset(self, hkey, update):
		new_update = {}
		if len(update) == 0:
			return
		for k, v in update.items():
			new_update[k] = self.encoder(v)
		return self.redis.hmset(hkey, new_update)

	def hdel(self, hkey, key):
		return self.redis.hdel(hkey, key)

	def hkeys(self, hkey):
		return self.redis.hkeys(hkey)

class RedisKeyedObject(object):
	def __init__(self, coder, key):
		self.coder = coder
		self.key = key

	def pop(self, timeout=0, block=False):
		return self.coder.pop(self.key, timeout=timeout, block=block)

	def hget(self, key):
		return self.coder.hget(self.key, key)

	def hgetall(self):
		return self.coder.hgetall(self.key)

	def hmget(self, keys):
		return self.coder.hmget(self.key, keys)

	def hset(self, key, value):
		return self.coder.hset(self.key, key, value)

	def hmset(self, update):
		return self.coder.hmset(self.key, update)

	def hdel(self, key):
		return self.coder.hdel(self.key, key)

	def hkeys(self):
		return self.coder.hkeys(self.key)
