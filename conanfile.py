from conans import ConanFile, CMake, tools
import os


class USDConan(ConanFile):
    name = "USD"
    version = "23.08"
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
        "opensubdiv:with_opengl": True,
        "opensubdiv:with_metal": True
    }
    generators = "cmake"
    short_paths = True

    requires = ("boost/1.76.0", "zlib/1.2.11", "onetbb/2020.3")

    def source(self):
        tools.get(
            "https://github.com/PixarAnimationStudios/OpenUSD/archive/v{}.zip".format(
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
                {"OPENSUBDIV_ROOT_DIR": self.deps_cpp_info["opensubdiv"].rootpath}
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
        cmake.configure(source_folder="OpenUSD-{}".format(self.version))
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
            self.requires("opensubdiv/3.5.0@")

    def package_info(self):
        self.cpp_info.libs = [
            "usd_ar",
            "usd_arch",
            "usd_gf",
            "usd_js",
            "usd_kind",
            "usd_ndr",
            "usd_pcp",
            "usd_plug",
            "usd_sdf",
            "usd_sdr",
            "usd_tf",
            "usd_trace",
            "usd_usd",
            "usd_usdGeom",
            "usd_usdHydra",
            "usd_usdLux",
            "usd_usdMedia",
            "usd_usdRender",
            "usd_usdRi",
            "usd_usdShade",
            "usd_usdSkel",
            "usd_usdUI",
            "usd_usdUtils",
            "usd_usdVol",
            "usd_vt",
            "usd_work",
        ]
        if self.options.with_imaging:
            self.cpp_info.libs.extend(
                [
                    "usd_cameraUtil",
                    "usd_garch",
                    "usd_glf",
                    "usd_hd",
                    "usd_hdSt",
                    "usd_hdx",
                    "usd_hf",
                    "usd_hgi",
                    "usd_hgiGL",
                    "usd_hgiInterop",
                    "usd_hio",
                    "usd_pxOsd",
                    "usd_usdAppUtils",
                    "usd_usdImaging",
                    "usd_usdImagingGL",
                    "usd_usdRiImaging",
                    "usd_usdSkelImaging",
                    "usd_usdVolImaging",
                ]
            )

    def imports(self):
        self.copy("*.dll", "", "bin")
        self.copy("*.dylib", "", "lib")


