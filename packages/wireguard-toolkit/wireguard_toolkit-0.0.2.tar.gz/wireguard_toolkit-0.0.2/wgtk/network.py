import types
import shutil
import pathlib
import ipaddress

from . file import File
from . import WireGuard
from . template import Template



class Peer:

	@classmethod
	def Create(self, network, name, configuration):
		address = configuration['address']
		address = self.Address.Create(address)
		return self(network, name, address)

	class Path:

		def __init__(self, peer):
			self.root = peer.network.path.root / peer.name

			self.config = types.SimpleNamespace()
			self.config.wg = self.root / f'{peer.name}.conf'

			self.script = types.SimpleNamespace()
			self.script.root = self.root / 'control'
			self.script.install = self.script.root / 'install'
			self.script.start   = self.script.root / 'start'
			self.script.stop    = self.script.root / 'stop'
			self.script.systemd = self.script.root / f'wg-{peer.network.name}.service'

	class Address:

		@classmethod
		def Create(self, block):
			interface = ipaddress.ip_interface(block['interface'])
			host = block['host'] if 'host' in block else None
			if host is not None:
				host = host.rsplit(':', 1)
				if len(host) != 2:
					assert False, f'Host address `{block["host"]}` requires a port'
				host = (ipaddress.ip_address(host[0]), int(host[1]))

			relay = {}
			if 'relay' in block:
				for address, peer_name in block['relay'].items():
					address = ipaddress.ip_network(address)
					relay[address] = peer_name

			return self(interface=interface, host=host, relay=relay)

		def __init__(self, interface, host=None, relay={}):
			self.interface = interface
			self.host = host
			self.relay = relay

	def __init__(self, network, name, address):
		self.name = name
		self.address = address
		self.network = network

		self.hosts   = []
		self.clients = []

		self.key = WireGuard.Key()
		self.path = self.Path(self)
		self.is_host = self.address.host is not None
		self.peers = self.clients if self.is_host else self.hosts

	def resolve(self):
		for address, peer_name in self.address.relay.items():
			assert self.name != peer_name
			# We probably don't want a connection
			# relaying all connections to itself

			assert peer_name in self.network
			# The peer should be defined

			peer = self.network[peer_name]
			self.address.relay[address] = peer

			# @TODO:
			# Feels like some of this wierd
			# double calculation can be avoided?

			if peer.is_host:
				if peer not in self.hosts:
					self.hosts.append(peer)

			if self.is_host:
				if peer not in self.clients:
					self.clients.append(peer)

	def generate_keys(self):
		if self.is_host:
			self.key.generate(preshared={peer.name: None for peer in self.clients})
		else:
			self.key.generate()

	def generate_wg_config_interface(self):
		config = WireGuard.Configuration.Interface()
		if self.is_host:
			config['ListenPort'] = str(self.address.host[1])
		config['PrivateKey'] = self.key.private
		return config

	def generate_wg_config_peer(self, peer):
		config = WireGuard.Configuration.Peer()

		# @TODO: debug code. remove
		# config['Name'] = peer.name

		config['PublicKey'] = peer.key.public

		if peer in self.hosts:
			endpoint = f'{peer.address.host[0]}:{peer.address.host[1]}'
			config['Endpoint'] = endpoint
			psk = peer.key.preshared[self.name]

		elif self.is_host:
			psk = self.key.preshared[peer.name]

		config['PresharedKey'] = psk

		allowed_ips = [str(i) for i, p in self.address.relay.items() if p is peer]
		allowed_ips = ', '.join(allowed_ips)
		config['AllowedIPs'] = allowed_ips

		return config

	def generate_wg_config(self):
		config_interface = self.generate_wg_config_interface()
		configs_peer = [self.generate_wg_config_peer(_) for _ in self.peers]

		config = WireGuard.Configuration(config_interface, configs_peer)
		File.Write(self.path.config.wg, config)

	def generate_systemd_service(self):
		unit_file = Template('systemd.service')({'network_name': self.network.name})
		File.Write(self.path.script.systemd, unit_file)

	def generate_install_script(self):
		return self.path.script.install, Template('install.bash')({'network_name': self.network.name})

	def generate_start_script(self):
		return self.path.script.start, Template('start.bash')({
			'network_name': self.network.name,
			'peer_name': self.name,
			'interface_address': str(self.address.interface)
		})

	def generate_stop_script(self):
		return self.path.script.stop, Template('stop.bash')({'network_name': self.network.name})


	def __repr__(self):
		return \
f'''Peer `{self.name}`
--- Hosts
  {[_.name for _ in self.hosts]}

--- Clients
  {[_.name for _ in self.clients]}
'''



class Network:

	@classmethod
	def Create(self, configuration):
		name = configuration['network']['name']

		network = self(name)
		for peer_name, peer_block in configuration['network']['peer'].items():
			peer = Peer.Create(network, peer_name, peer_block)
			network.insert(peer)

		return network

	class Path:

		def __init__(self, network):
			self.root = pathlib.Path(network.name)

	def __init__(self, name):
		self.name = name
		self.peer = {}

		self.path = self.Path(self)
		self.hosts = []

	def insert(self, peer):
		self.peer[peer.name] = peer

	def resolve(self):
		for peer in self:
			peer.resolve()
			if peer.is_host:
				self.hosts.append(peer)

	def print(self):
		for peer in self:
			print(peer)

	def __iter__(self):
		return iter(self.peer.values())

	def __getitem__(self, *args, **kwargs):
		return self.peer.__getitem__(*args, **kwargs)

	def __contains__(self, *args, **kwargs):
		return self.peer.__contains__(*args, **kwargs)
