from conans import ConanFile, CMake, tools
import os


class USDConan(ConanFile):
    name = "USD"
    version = "20.08"
    license = "<Put the package license here>"
    author = "<Put your name here> <And your email here>"
    url = "<Package recipe repository url here, for issues about the package>"
    description = "<Description of USD here>"
    topics = ("<Put some tag here>", "<here>", "<and here>")
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "with_imaging": [True, False], }
    default_options = {"shared": False, "with_imaging": True}
    generators = "cmake"
    exports_sources = 'patch_find_glew_to_find_debug_libs.patch'

    requires = (
        "boost/1.70.0",
        "zlib/1.2.11",
        "tbb/2020.2",
        "glew/2.1.0"
    )

    def source(self):
        tools.get("https://github.com/PixarAnimationStudios/USD/archive/v{}.tar.gz".format(self.version))
        tools.patch(patch_file='patch_find_glew_to_find_debug_libs.patch')

    def _configure_cmake(self):
        os.environ.update({
            "TBB_ROOT": self.deps_cpp_info["tbb"].rootpath,
            "GLEW_LOCATION": self.deps_cpp_info["glew"].rootpath,
            "OPENSUBDIV_ROOT_DIR": self.deps_cpp_info["OpenSubdiv"].rootpath
        })
        cmake = CMake(self)
        cmake.definitions["PXR_ENABLE_PYTHON_SUPPORT"] = False
        cmake.definitions["PXR_BUILD_IMAGING"] = self.options.with_imaging
        cmake.definitions["BUILD_SHARED_LIBS"] = self.options.shared
        cmake.definitions["PXR_BUILD_TESTS"] = False
        cmake.definitions["PXR_BUILD_EXAMPLES"] = False
        cmake.definitions["PXR_ENABLE_PTEX_SUPPORT"] = False
        cmake.definitions["PXR_ENABLE_METAL_SUPPORT"] = False
        cmake.configure(source_folder="USD-{}".format(self.version))
        return cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        cmake = self._configure_cmake()
        cmake.install()

    def requirements(self):
        if self.options.with_imaging:
            self.requires("glew/2.1.0")
            self.requires("OpenSubdiv/3.4.3@latios96/stable")

    def package_info(self):
        self.cpp_info.libs = [
            "ar",
            "pcp",
            "usd",
            "usdRi",
            "vt",
            "arch",
            "plug",
            "usdGeom",
            "usdShade",
            "work",
            "gf",
            "sdf",
            "usdHydra",
            "usdSkel",
            "js",
            "sdr",
            "usdLux",
            "usdUI",
            "kind",
            "tf",
            "usdMedia",
            "usdUtils",
            "ndr",
            "trace",
            "usdRender",
            "usdVol"]

    def imports(self):
        self.copy("*.dll", "", "bin")
        self.copy("*.dylib", "", "lib")
