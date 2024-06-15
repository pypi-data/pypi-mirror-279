import subprocess

from . file import File
from . template import Template



class Bash:

	def __init__(self, path):
		self.path = path
		self.commands = []
		self.header = Template('generate_keys_header.bash')()

	def insert(self, command):
		self.commands.append(command)

	def run(self):
		File.Write(self.path, self)
		result = subprocess.run(['bash', self.path.as_posix()], check=True)
		self.path.unlink()

	def __str__(self):
		return self.header + '\n'.join(self.commands)
