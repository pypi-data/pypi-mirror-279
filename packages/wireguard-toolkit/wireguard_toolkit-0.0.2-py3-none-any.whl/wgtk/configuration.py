import yaml
import pathlib



class Configuration:

	def __init__(self, path):
		self.path = pathlib.Path(path)
		self.load()
		self.validate()

	def load(self):
		# @TODO
		# No error handling lol
		with open(self.path, 'r') as source:
			self.source = yaml.load(source, Loader=yaml.CSafeLoader)

	def validate(self):
		# @TODO
		# Very basic validation of the
		# structure of the document.
		# No error messages yet, so
		# these are going to be a bit hard
		# to decode for the user.
		assert 'network' in self.source
		network = self.source['network']
		assert type(network) is dict

		name = network['name']
		assert type(name) is str


		assert 'peer' in network
		peers = network['peer']
		assert type(peers) is dict
		assert len(peers) >= 2

		for peer in peers.values():
			assert type(peer) is dict
			assert 'address' in peer
			address = peer['address']
			assert type(address) is dict
			assert 'interface' in address
