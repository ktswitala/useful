
class Nameserver(object):
	def __init__(self):
		self.nsURI, self.nsDaemon, _ = Pyro4.naming.startNS()
		self.nsProxy = Pyro4.Proxy(self.nsURI)

	def nameserver_thread(self):
		self.nsDaemon.requestLoop()

	def start(self):
		self.ns_thread = threading.Thread(target=self.nameserver_thread)
		self.ns_thread.start()

	def shutdown(self):
		self.nsDaemon.shutdown()

class Daemon(object):
	def __init__(self, ns=None):
		self.daemon = Pyro4.Daemon()
		if ns is None:
			self.nsProxy = Pyro4.naming.locateNS()
		else:
			self.nsProxy = ns

	def daemon_thread(self):
		if hasattr(self, 'on_start'):
			self.on_start(self)
		self.daemon.requestLoop()
		if hasattr(self, 'on_shutdown'):
			self.on_shutdown(self)

	def start(self):
		self.daemon_thread = threading.Thread(target=self.daemon_thread)
		self.daemon_thread.start()

	def publish(self, name, object):
		uri = pyro.daemon.register(object)
		pyro.nsProxy.register(name, uri)

	def shutdown(self):
		self.daemon.shutdown()
