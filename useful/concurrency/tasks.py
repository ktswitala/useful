
class DelayedTask(object):
	def __init__(self, fn):
		self.fn = fn
		self.state = "waiting"
		self.task = None

	def update(self, ctx):
		if self.state == "waiting":
			self.task = self.fn()
			self.state = "active"
		if self.state == "active":
			self.task.update(ctx)
			if self.task.finished():
				self.state = "finished"

	def finished(self):
		return self.state == "finished"

class SequenceTask(object):
	def __init__(self, *tasks):
		self.tasks = tasks
		self.current_task = 0

	def update(self, ctx):
		if self.current_task >= len(self.tasks):
			return
		task = self.tasks[self.current_task]
		task.update(ctx)
		if task.finished():
			self.current_task += 1

	def finished(self):
		return self.current_task >= len(self.tasks)
