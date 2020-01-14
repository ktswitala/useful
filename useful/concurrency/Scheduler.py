
import useful

class EventTime(object):
	def __init__(self):
		self.pqueue = []
		self.periods = {}

	def schedule(self, now, event, period, start_time=None):
		if event in self.periods:
			raise Exception("event exists")
		if start_time is None:
			start_time = now
		self.periods[event] = period
		heapq.heappush(self.pqueue, (start_time+period, event))

	def find_ready(self, now, dup=False):
		if dup is False:
			return self.find_ready_no_dup(now)
		elif dup is True:
			return self.find_ready_dup(now)

	def find_ready_no_dup(self, now):
		ready = []
		while True:
			if len(self.pqueue) == 0:
				break
			t, event = self.pqueue[0]
			if now > t:
				heapq.heappop(self.pqueue)
				ready.append(event)
			else:
				break
		for event in ready:
			heapq.heappush(self.pqueue, (now+self.periods[event], event))
		return ready

	def find_ready_dup(self, now):
		ready = []
		while True:
			if len(self.pqueue) == 0:
				break
			t, event = self.pqueue[0]
			if now > t:
				heapq.heappushpop(self.pqueue, (t+self.periods[event], event))
				ready.append(event)
			else:
				break
		return ready

class Scheduler(object):
	def __init__(self):
		self.clients = {}

		self.client_list = useful.LinkedList()
		self.client_list.register_next_fn( *useful.meta.create_getset('next_client') )
		self.client_list.register_prev_fn( *useful.meta.create_getset('prev_client') )

		self.itr = self.client_list.iter()

	def add_client(self, client_info):
		if client_info.name in self.clients:
			client_info.error("Scheduler", "add_client - client already exists")
			return
		else:
			self.clients[client_info.name] = client_info
			self.client_list.append(client_info)

			client_info.added()

	def remove_client(self, client_info):
		if client.name in self.clients:
			del self.clients[client_info.name]
			self.client_list.remove(client_info)
			client_info.removed()
		else:
			client_info.error("Scheduler", "remove_client - client not registered")

	def next(self):
		client = self.client_list.iter_next(self.itr)
		if client is None:
			if self.client_list.is_empty():
				return None
			else:
				self.client_list.iter_reset(self.itr)
				client = self.client_list.iter_next(self.itr)
		return client

class TimesliceScheduler(Scheduler):
	def __init__(self, slice_size=None):
		super().__init__(self)
		self.slice_size = slice_size
		self.slice_start = None
		self.slice_end = None

	def start(self):
		self.slice_start = time.time()
		self.slice_end = self.slice_start + slice_size
		self.current_client = self.next()

	def update(self):
		now = time.time()
		if now > self.slice_end:
			self.slice_start = time.time()
			self.slice_end = self.slice_start + slice_size
			self.current_client = self.next()
			self.notify(self.current_client, self.slice_start, self.slice_end)

def run_time_slice(action, start_time, end_time):
	while time.time() < start_time:
		time.sleep(0.1)
	worst_case_execute = 0.0
	while time.time() + worst_case_execute < end_time:
		time_start = time.time()
		action()
		time_taken = time.time() - time_start
		if time_taken > worst_case_execute:
			worst_case_execute = time_taken
