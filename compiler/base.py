class Base(object):
	def __init__(self, name, options):
		self.name = name
		self._options = options
		self._config = dict(
			CXXFLAGS=[
				"-std=c++11",
				"-Wall",
				"-Wextra",
				"-pedantic",
				"-O2",
				"-pipe",
				"-pthread",
				"-Wreorder",
				"-Wmissing-field-initializers",
				# soci uses deprecated auto_ptr extensively, so
				"-Wno-deprecated-declarations",
				# easylogging warnings
				# "-Wno-pessimizing-move",
			]
		)

	def get_bin(self):
		return self.name

	def set_value(self, key, value, replace=False):
		if key not in self._config or replace:
			self._config[key] = []
		self._config[key] = self._config.get(key, [])
		self._config[key].append(value)

	def get_value(self, key, default=None):
		return self._config.get(key, default)
		if key in self._config:
			return " ".join(self._config[key])
		return default

	def as_dict(self):
		result = {}
		for k in self._config:
			result[k] = self.get_value(k, [])
		return result

	def configure(self, platform):
		# print("Configuring compiler '%s' for platform '%s'" % (self.name, platform))
		pass

	def get_debug_flags(self):
		return ["-g"]

	def get_libs(self):
		return []

	def get_static_libs(self):
		return []

	def get_linkflags(self):
		return ["-pthread"]

	def get_static_linkflags(self):
		return [
			"--static",
			"-static-libstdc++",
			"-pthread",
		]
