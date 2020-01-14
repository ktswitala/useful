
class RoundRobin(object):
	def __init__(self):
		self.elements = []
		self.current_element = 0

	def next(self):
		if len(self.elements) == 0:
			return None
		if self.current_element > len(self.elements)-1:
			self.current_element = len(self.elements)-1
		element = self.elements[self.current_element]
		self.current_element = (self.current_element+1) % len(self.elements)
		return element
