
class ThreadUpdateLoop(object):
	def __init__(self):
		self.fns = {}
		self.failed_fns = {}
		self.delay = 0.1
		self.running = True
		self.thread = threading.Thread(target=self.loop)

	def start(self):
		self.start_time = time.time()-1
		self.idle_time = 0
		self.fn_usage = collections.defaultdict(lambda: 0)
		self.thread.start()

	def usage(self):
		total_time = time.time() - self.start_time
		return (total_time - self.idle_time) / total_time

	def loop(self):
		while self.running:
			items = self.fns.items()
			for name, fn in items:
				if name in self.failed_fns:
					continue
				try:
					usage_start = time.time()
					fn()
					self.fn_usage[name] += usage_start - time.time()
				except Exception as e:
					print("update loop {0} failed".format(name))
					traceback.print_exc()
					self.failed_fns[name] = fn
			start_sleep = time.time()
			time.sleep(self.delay)
			self.idle_time += time.time() - start_sleep

	def add(self, name, fn):
		self.fns[name] = fn

	def stop(self):
		self.running = False

	def __del__(self):
		self.stop()
