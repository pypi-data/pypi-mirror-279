import string
import pathlib



class Path:
	Root = pathlib.Path(__file__).parent



class Template:

	def __init__(self, name):
		self.path_initialize(name)
		self.load()

	def path_initialize(self, name):
		path = Path.Root / name
		self.path_validate(name, path)
		self.path = path

	def path_validate(self, name, path):
		if not path.exists():
			raise KeyError(f'Template `{name}` does not exist')

	def load(self):
		with open(self.path, 'r') as f:
			self.source = string.Template(f.read())

	def __call__(self, mapping={}):
		return self.source.substitute(mapping)
