import sys
import os
from collections import OrderedDict
from buildsys.builder import Builder

AddOption(
	"--compiler",
	dest="compiler",
	action="store",
	choices=["clang", "gcc"],
	default="clang",
	help="compiler to use")

AddOption(
	"--enable-debug",
	dest="debug_build",
	action="store_true",
	default=False,
	help="debug build")

AddOption(
	"--static-build",
	dest="static_build",
	action="store_true",
	default=False,
	help="link statically")

AddOption(
	"--with-tests",
	dest="build_tests",
	action="store_true",
	default=False,
	help="Build tests")


class Dirs(object):
	build = "#build"
	objects = "%s/objs" % build
	target = "%s/target" % build
	source = "#src"
	source_service = os.path.join("#src", "dbl")
	source_dblclient = os.path.join("#src", "dblclient")
	source_test = os.path.join("#src", "test")
	extern_include = os.path.join(os.environ["VIRTUAL_ENV"], "include")
	project_source = source
	destdir = "#bin"
	lib_destdir = "#lib"


MAIN_TARGET_NAME = "program"
THIS_PLATFORM = os.uname()[0].lower()

builder_options = dict()
builder = Builder(builder_options, "clang")

if GetOption("debug_build"):
	builder.add_define("DEBUG")
	builder.set_debug_build()

builder.add_lib_path(
	os.path.join(os.environ["VIRTUAL_ENV"], "lib"),
	os.path.join(os.environ["VIRTUAL_ENV"], "lib64"),
)

builder.add_library(
	# "boost_system",
	# "boost_program_options",
	# "boost_filesystem",
)

builder.add_include_path(Dirs.source, Dirs.extern_include)

build_options = {}

if GetOption("static_build"):
	builder.set_static_build()
	MAIN_TARGET_NAME += "-static"

env = Environment(**builder.as_dict())
env["ENV"]["TERM"] = os.environ.get("TERM")


def extend_env(src_env, params):
	dest = src_env.Clone()
	entities = ["CXXFLAGS", "CPPPATH", "LIBS", "LIBPATH"]
	params = params if isinstance(params, list) else [params]
	for skel in params:
		for item in entities:
				if not dest.get(item):
					dest[item] = []
				items = skel.get(item)
				if items:
					dest[item].extend(items if isinstance(items, list) else [items])
	for item in entities:
		# using OrderedDict, as set reorders elements causing linking error...
		dest[item] = OrderedDict.fromkeys(dest[item]).keys()
	return dest

translation_units = {
	# "myprog/main": {},
}

platform_translation_units = {
	"linux": {
		"dbl/config/unix": {},
		"dbl/service/configurator/unix" : {},
		"dbl/service/unix" : {},
		"dbl/service/worker/unix" : {},
	}
}

translation_units.update(
	platform_translation_units[THIS_PLATFORM]
)

target_objects = []

for tunit in sorted(translation_units):
	tunit_def = translation_units[tunit]
	tunit_env = tunit_def.get("env", env).Clone()
	extend_env(tunit_env, {
		"CPPPATH" : tunit_def.get("cpppath", []),
		"LIBS" : tunit_def.get("libs", []),
		"LIBPATH" : tunit_def.get("libpath", []),
	})
	obj = tunit_env.SharedObject(
		os.path.join(Dirs.objects, tunit) + ".o",
		os.path.join(Dirs.project_source, tunit) + ".cxx"
	)
	target_objects.append(obj)

if GetOption("build_tests"):
	test_sconscripts = {
		"program": os.path.join(Dirs.source_test,  "SConscript"),
	}

	exports = [
		"extend_env", "env", "Dirs",
		"translation_units", "target_objects",
		"THIS_PLATFORM", 
	]

	for test_builder in test_sconscripts:
		SConscript(
			test_sconscripts[test_builder],
			exports=exports,
			variant_dir=os.path.join(Dirs.build, "tests", test_builder),
			duplicate=0
		)
