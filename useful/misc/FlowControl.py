
class SizedElementQueue(object):
	def __init__(self, size_element, current_size):
		self.size_element = size_element
		self.current_size = current_size

	def push(self, e):
		self.current_size += self.size_element(e)

	def pop(self, e):
		self.current_size -= self.size_element(e)

class SizeMonitor(object):
	def __init__(self, get_current_size):
		self.min_size = 0
		self.max_size = None
		self.get_current_size = get_current_size

	def has_room(self, size):
		if size + self.get_current_size() > self.max_size:
			return False
		else:
			return True

	def status(self):
		size = self.get_current_size()
		if size > self.max_size:
			return "hi"
		elif size < self.min_size:
			return "lo"
		else:
			return "med"

class FlowRateControl(object):
	def __init__(self):
		self.rate_history = History(25, self.add_history, self.remove_history, self.update_history)
		self.total_flow = 0
		self.total_time = 0.0
		self.flow_per_time = None

	def add_history(self, v):
		amount, time = v
		self.total_flow += amount
		self.total_time += time

	def remove_history(self, v):
		amount, time = v
		self.total_flow -= amount
		self.total_time -= time

	def update_history(self):
		if self.total_time == 0.0:
			self.flow_per_time = None
		else:
			self.flow_per_time = self.total_flow / self.total_time

	def update(self, amount=None, time=None):
		self.rate_history.add( (amount, time) )

	def amount_needed(self, time_requested):
		if self.flow_per_time in [None, 0]:
			return None
		else:
			return self.flow_per_time * time_requested
