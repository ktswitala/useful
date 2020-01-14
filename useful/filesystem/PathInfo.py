
class PathInfo(object):
	def __init__(self, full_path):
		self.full_path = full_path
		self.stat = None
		self.last_stat = None
		self.stat_error = None

	def update_stat(self):
		try:
			self.stat = os.stat(self.full_path)
		except Exception as e:
			print(e)
			self.stat_error = e
			self.stat = None
		self.last_stat = time.time()

	def filetype(self):
		if self.stat is None:
			self.update_stat()
		if self.stat is None:
			return "unknown"
		if stat.S_ISDIR(self.stat.st_mode):
			return "dir"
		elif stat.S_ISREG(self.stat.st_mode):
			return "reg"
		else:
			return "unknown"

	def get_entries(self):
		new_entries = []
		try:
			if self.filetype() == "dir":
				new_entries = [os.path.join(self.full_path, basename) for basename in os.listdir(self.full_path)]
		except PermissionError:
			pass
		except:
			raise

		return new_entries
