from conans import ConanFile, CMake, tools
import os


class USDConan(ConanFile):
    name = "USD"
    version = "21.02"
    license = "Apache-2.0"
    author = "Jan Honsbrok <jan.honsbrok@gmail.com>"
    url = "https://github.com/Latios96/conan-USD"
    description = "Universal Scene Description (USD) is an efficient, scalable system for authoring, reading, and streaming time-sampled scene description for interchange between graphics applications."
    topics = ("cgi", "vfx", "dcc", "usd")
    settings = "os", "compiler", "build_type", "arch"
    options = {
        "shared": [True, False],
        "with_imaging": [True, False],
    }
    default_options = {
        "shared": True,
        "with_imaging": True,
        "boost:layout": "b2-default",  # todo do we need this?
    }
    generators = "cmake"
    short_paths = True

    requires = ("boost/1.70.0", "zlib/1.2.11", "onetbb/2020.3")

    def source(self):
        tools.get(
            "https://github.com/PixarAnimationStudios/USD/archive/v{}.zip".format(
                self.version
            )
        )

    def _configure_cmake(self):
        os.environ.update(
            {
                "TBB_ROOT": self.deps_cpp_info["onetbb"].rootpath,
            }
        )

        if self.options.with_imaging:
            os.environ.update(
                {"OPENSUBDIV_ROOT_DIR": self.deps_cpp_info["OpenSubdiv"].rootpath}
            )

        cmake = CMake(self)
        if self.settings.build_type == "Debug":
            cmake.definitions["TBB_USE_DEBUG_BUILD"] = True
        cmake.definitions["PXR_ENABLE_PYTHON_SUPPORT"] = False
        cmake.definitions["PXR_BUILD_IMAGING"] = self.options.with_imaging
        cmake.definitions["BUILD_SHARED_LIBS"] = self.options.shared
        cmake.definitions["PXR_BUILD_TESTS"] = False
        cmake.definitions["PXR_BUILD_EXAMPLES"] = False
        cmake.definitions["PXR_ENABLE_PTEX_SUPPORT"] = False
        cmake.definitions["PXR_ENABLE_METAL_SUPPORT"] = False
        cmake.definitions["Boost_USE_STATIC_LIBS"] = True
        cmake.definitions["-DBOOST_AUTO_LINK_SYSTEM"] = True
        cmake.configure(source_folder="USD-{}".format(self.version))
        return cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        cmake = self._configure_cmake()
        cmake.install()

        if self.settings.os == "Windows":
            self.copy("**.dll", "bin", "", keep_path=False)
            self.copy("**.lib", "bin", "", keep_path=False)  # todo do we need this?

    def requirements(self):
        if self.options.with_imaging:
            self.requires("OpenSubdiv/3.4.4@latios96/stable")

    def package_info(self):
        self.cpp_info.libs = [
            "ar",
            "arch",
            "gf",
            "js",
            "kind",
            "ndr",
            "pcp",
            "plug",
            "sdf",
            "sdr",
            "tf",
            "trace",
            "usd",
            "usdGeom",
            "usdHydra",
            "usdLux",
            "usdMedia",
            "usdRender",
            "usdRi",
            "usdShade",
            "usdSkel",
            "usdUI",
            "usdUtils",
            "usdVol",
            "vt",
            "work",
        ]
        if self.options.with_imaging:
            self.cpp_info.libs.extend(
                [
                    "cameraUtil",
                    "garch",
                    "glf",
                    "hd",
                    "hdSt",
                    "hdx",
                    "hf",
                    "hgi",
                    "hgiGL",
                    "hgiInterop",
                    "hio",
                    "pxOsd",
                    "usdAppUtils",
                    "usdImaging",
                    "usdImagingGL",
                    "usdRiImaging",
                    "usdSkelImaging",
                    "usdVolImaging",
                ]
            )

    def imports(self):
        self.copy("*.dll", "", "bin")
        self.copy("*.dylib", "", "lib")
