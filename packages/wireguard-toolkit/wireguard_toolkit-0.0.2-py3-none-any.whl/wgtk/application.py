import os
import shutil
import pathlib
import datetime

from . file import File
from . network import Network
from . template import Template 
from . configuration import Configuration



class Application:


	class GenerateTemplate:

		def run(self):
			template = Template('network.yml')

			context = {
				'application_name': 'WireGuard Toolkit',
				'application_time': str(datetime.datetime.now())
			}

			print(template(context))


	class GenerateConfiguration:

		def __init__(self, path):
			os.umask(0o077)
			self.configuration = Configuration(path)
			self.network = Network.Create(self.configuration.source)

		def run(self):
			self.network.resolve()
			self.output_directory_delete_if_exists()
			self.output_directory_create()
			self.output_generate_peer_keys()

			self.output_generate_peer_configs()
			self.output_generate_scripts()

		def create_script(self, path, value):
			File.Write(path, value, mode=0o700)

		def output_directory_delete_if_exists(self):
			path = self.network.path.root
			shutil.rmtree(path, ignore_errors=True)
			path.unlink(missing_ok=True)
			if path.exists():
				raise RuntimeError(f"Could not delete {path}. Something is wrong")

		def output_directory_create(self):
			for peer in self.network:
				peer.path.script.root.mkdir(parents=True)

		def output_generate_peer_keys(self):
			for peer in self.network:
				peer.generate_keys()

		def output_generate_peer_configs(self):
			for peer in self.network:
				peer.generate_wg_config()

		def output_generate_scripts(self):
			for peer in self.network:
				peer.generate_systemd_service()
				fns = (peer.generate_start_script, peer.generate_stop_script, peer.generate_install_script)
				for fn in fns:
					self.create_script(*fn())
