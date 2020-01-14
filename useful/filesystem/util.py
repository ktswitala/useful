
def mkdir(path):
	if not os.path.exists(path):
		os.makedirs(path)

def remove_dir_files(d):
	for filename in os.listdir(d):
		full_path = os.path.join(d, filename)
		if os.path.isfile(full_path):
			os.remove(full_path)
		elif os.path.isdir(full_path):
			shutil.rmtree(full_path)

def move_files(src_filenames, src_root_path, dest_root_path):
	for src_filename in src_filenames:
		if not within(src_root_path, src_filename):
			raise Exception("src_filename {0} is not inside src_path {1}".format(filename, src_root_path))
		dest_filename = relative_move(src_root_path, dest_root_path, src_filename)
		if not os.path.exists(os.path.dirname(dest_filename)):
			os.makedirs(os.path.dirname(dest_filename))
		print("{0} ---> {1}".format(src_filename, dest_filename))
		if os.path.exists(src_filename):
			raise Exception("{0} already exists".format(dest_filename))
		shutil.move(src_filename, dest_filename)

def relative_move(src_root_path, dest_root_path, path):
	path = pathlib.PurePosixPath(path)
	relpath = str(path.relative_to(src_root))
	move_to_path = os.path.join(dest_root, relpath)
	return move_to_path

def archive_copy(src_file, dest_file):
	easy_popen(['/bin/mkdir', '-p', os.path.dirname(dest_file)])
	if os.path.isdir(dest_file):
		dest_file = os.path.dirname(dest_file)
	sp = easy_popen(['/bin/cp', '-auf', src_file, dest_file])

def ctime_to_mtime(path):
	stat = os.stat(path)
	atime = stat.st_atime
	mtime = stat.st_ctime

	os.utime(path, (atime, mtime))
