


class File:

	@classmethod
	def Read(self, path, strip=False):
		with open(path, 'r') as f:
			g = f.read()
			if strip:
				return g.strip()
			return g

	@classmethod
	def Write(self, path, instance, mode=None):
		with open(path, 'w') as f:
			f.write(str(instance))
		if mode is not None:
			path.chmod(mode)
