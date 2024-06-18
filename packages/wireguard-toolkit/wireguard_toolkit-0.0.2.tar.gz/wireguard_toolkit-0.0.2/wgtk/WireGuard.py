import io
import subprocess
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



class Key:

	@classmethod
	def Run(self, command, input=None):
		p = subprocess.Popen(
			command,
			stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE,
			text=True,
		)

		if input is None:
			key = p.communicate()[0].strip()

		else:
			key = p.communicate(input=input)[0].strip()

		t = type(key)
		assert t is str, f'Error: key is not the right type ["{t}": {key}]'

		l = len(key)
		assert l == 44, f'Error: key is not the right length ["{l}": {key}]'

		return key

	def __init__(self):
		self.private = None
		self.public = None
		self.preshared = None

	def generate(self, preshared=None):
		self.preshared = preshared
		self.generate_key_private()
		self.generate_key_public()
		self.generate_keys_preshared()

	def generate_key_private(self):
		self.private = self.Run(['wg', 'genkey'])

	def generate_key_public(self):
		self.public = self.Run(['wg', 'pubkey'], input=self.private)

	def generate_keys_preshared(self):
		if self.preshared is None:
			return

		for name in self.preshared:
			self.preshared[name] = self.Run(['wg', 'genpsk'])
