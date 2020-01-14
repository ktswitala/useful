
import os
import time
import heapq

import threading
import queue
import dill

class Module(dict):
	pass

def dupdate_obj(obj, d, keys=None):
	if keys is None:
		keys = d.keys()
	for key in keys:
		setattr(obj, key, d[key])

def load_dir_to_obj(source_dir, locals, obj_name):
	m = Module()
	before = set(locals.keys())
	for filename in os.listdir(source_dir):
		path = os.path.join(source_dir, filename)
		f = open(path, "r")
		co = compile(f.read(), path, 'exec')
		f.close()
		exec(co, globals(), locals)
	added = set(locals.keys()) - before
#	print(source_dir, added)
	for k in added:
		locals[k].__name__ = "{0}.{1}".format(obj_name, locals[k].__name__)
#		s = locals[k].__name__
#		if hasattr(locals[k], '__qualname__'):
#			locals[k].__qualname__ = "{0}.{1}".format(obj_name, locals[k].__qualname__)
#			s += " {0}".format(locals[k].__qualname__)
#		print(s)
		setattr(m, k, locals[k])
		del locals[k]
	return m

def load_dir_to_dict(source_dir, locals):
	m = Module()
	before = set(locals.keys())
	for filename in os.listdir(source_dir):
		path = os.path.join(source_dir, filename)
		f = open(path, "r")
		co = compile(f.read(), path, 'exec')
		f.close()
		exec(co, globals(), locals)
	added = set(locals.keys()) - before
#	print(source_dir, added)
#	for k in added:
#		s = locals[k].__name__
#		if hasattr(locals[k], '__qualname__'):
#			s += " {0}".format(locals[k].__qualname__)
#		print(s)

load_dir_to_dict(os.path.join(__path__[0], "concurrency"), locals())
load_dir_to_dict(os.path.join(__path__[0], "database"), locals())
load_dir_to_dict(os.path.join(__path__[0], "filesystem"), locals())
load_dir_to_dict(os.path.join(__path__[0], "misc"), locals())
load_dir_to_dict(os.path.join(__path__[0], "object"), locals())
load_dir_to_dict(os.path.join(__path__[0], "scrape"), locals())
load_dir_to_dict(os.path.join(__path__[0], "struct"), locals())
load_dir_to_dict(os.path.join(__path__[0], "tree"), locals())

def resume_task():
	pass
def create_or_resume_task():
	pass
def run_tasks():
	pass
