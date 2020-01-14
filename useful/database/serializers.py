
import pickle
import json

class PickleSerializer(object):
	def data_to_bin(data):
		return pickle.dumps(data)

	def bin_to_data(bin):
		return pickle.loads(bin)

class JsonSerializer(object):
	def data_to_bin(data):
		return json.dumps(data)

	def bin_to_data(bin):
		return json.loads(bin)

def ascii_to_utf8(filename_from, filename_to):
	f = open(filename_from, "r")
	data = f.read()
	f.close()

	f = codecs.open(filename_to, "w", encoding="utf-8")
	f.write(data)
	f.close()
