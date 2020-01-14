
class CommandThread(object):
	def __init__(self):
		self.q = queue.Queue()
		self.running = True
		self.thread = threading.Thread(target=self.command_thread)

	def command_thread(self):
		while self.running:
			try:
				command, args, kwargs = self.q.get(timeout=0.5)
				command(*args, **kwargs)
			except queue.Empty:
				pass
			except Exception as e:
				import traceback
				traceback.print_exc()

	def commands_left(self):
		return self.q.qsize()

	def add(self, command, args=None, kwargs=None):
		if args is None:
			args = []
		if kwargs is None:
			kwargs = {}
		self.q.put( (command, args, kwargs) )

	def start(self):
		self.thread.start()

	def stop(self):
		self.running = False
		if self.thread.is_alive():
			self.thread.join()

class CommandThreadPool(object):
	def __init__(self, thread_count):
		self.thread_count = thread_count
		self.threads = []
		for i in range(0,self.thread_count):
			self.threads.append( CommandThread() )

	def start_threads(self):
		for thread in self.threads:
			thread.start()

	def total_pending_work(self):
		return sum([ct.commands_left() for ct in self.threads])

	def get_available_thread(self):
		return self.threads[argmin([ct.commands_left() for ct in self.threads])]

	def stop_threads(self):
		for thread in self.threads:
			thread.stop()

	def __del__(self):
		self.stop_threads()
