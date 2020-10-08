import sys

from cpt.packager import ConanMultiPackager

if __name__ == "__main__":
    builder = ConanMultiPackager(archs=["x86_64"])
    builder.add_common_builds()
    builder.build_policy = "missing"
    if sys.platform == "linux":
        for settings, options, env_vars, build_requires, reference in builder.items:
            settings["compiler.libcxx"] = "libstdc++11"
    builder.run()
