import io
import configparser



class Configuration:

	class Abstract:

		def __init__(self, section):
			self.parser = configparser.ConfigParser()
			self.parser.optionxform = str
			self.parser[section] = {}
			self.instance = self.parser[section]

		def __getitem__(self, *args, **kwargs):
			return self.instance.__getitem__(*args, **kwargs)

		def __setitem__(self, *args, **kwargs):
			return self.instance.__setitem__(*args, **kwargs)

		def __str__(self):
			with io.StringIO() as fake_file:
				self.parser.write(fake_file)
				return fake_file.getvalue()

	class Interface(Abstract):

		def __init__(self):
			super().__init__('Interface')

	class Peer(Abstract):

		def __init__(self):
			super().__init__('Peer')

	def __init__(self, interface=None, peers=[]):
		self.interface = interface or self.Interface()
		self.peers = peers

	def __str__(self):
		return str(self.interface) + ''.join([str(_) for _ in self.peers])
