
import os
import json
import pymongo
import time

# config:
# 'container' - name of container
# 'host', 'port'
# 'data_path' : where the data will be stored

class Mongo(object):
	def __init__(self, docker_client, config):
		self.docker_client = docker_client
		self.config = config

	def stop_container(self):
		container = self.docker_client.containers.get(self.config["container"])
		container.stop()
		container.remove()

	def clean(self):
		try:
			self.stop_container()
		except:
			pass

	def setup(self):
		current_dir = os.getcwd()
		environ = dict(os.environ)

		container = self.docker_client.containers.run(
			image="mongo",
			detach=True,
			ports={'27017/tcp': (self.config["host"], self.config["port"])},
			volumes={self.config["data_path"]:{"bind":"/data/db", "mode":"rw"}}
		)
		tries = 3
		while True:
			try:
				mongo_client = pymongo.MongoClient(self.config["host"], self.config["port"])
				db = mongo_client.get_database(name="admin")
				db.command("createUser", "admin", pwd="password", roles=["root"])
				break
			except Exception as e:
				print(type(e), e)
			if tries == 0:
				break
			tries -= 1

		container.stop()
		container.remove()

	def run(self):
		container = self.docker_client.containers.run(
			image="mongo", name=self.config["container"],
			command="--auth",
			detach=True,
			ports={'27017/tcp': (self.config["host"], self.config["port"])},
			volumes={self.config["data_path"]:{"bind":"/data/db", "mode":"rw"}}
		)
