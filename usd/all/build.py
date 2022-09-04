from cpt.packager import ConanMultiPackager

if __name__ == "__main__":
    builder = ConanMultiPackager(visual_versions=[16])
    builder.add_common_builds()
    builder.run()
