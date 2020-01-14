
def clean_path(path):
	_, subpath = os.path.splitdrive(path)
	return subpath.replace('\\','/').strip('/')

def split_path(path):
	rest = path
	split_nodes = []
	while True:
		rest, name = os.path.split(rest)
		if rest == '':
			raise Exception("relative paths not allowed")
		elif rest == '/' and name == '':
			break
		elif name == '':
			continue
		else:
			split_nodes.append(name)
	return list(split_nodes)

def valid_win_file_char(c):
	if c in ["/", "\\", ":", "|", "*", "?", "\""]:
		return False
	else:
		return True

def norm_path(path):
	if type(path) is str:
		l = path.strip('/').split('/')
	elif type(path) is list:
		l = list(path)
	return filter(lambda e: e != "", l)

def is_path_within_path(top_folder, bottom_folder):
	if os.path.commonprefix([top_folder, bottom_folder]) == top_folder:
		return True
	else:
		return False
