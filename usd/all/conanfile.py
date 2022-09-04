import functools
import os

from conan import ConanFile
from conan.tools.files import get, replace_in_file
from conans import CMake, tools
from conan.errors import ConanInvalidConfiguration

required_conan_version = ">=1.48.0"

# add CI fail-fast=False, add matrix for all options that are not related to dependencies, they should just be turned on by default
class UsdConan(ConanFile):
    name = "usd"
    license = "LicenseRef-LICENSE.txt"
    homepage = "https://github.com/PixarAnimationStudios/USD"
    url = "https://github.com/conan-io/conan-center-index"
    description = (
        "Universal Scene Description (USD) is an efficient, scalable system for authoring, reading, and streaming time-sampled scene description for interchange between graphics applications."
    )
    topics = ("cgi", "vfx", "animation", "scene description")

    settings = "os", "compiler", "build_type", "arch"
    options = {
        "shared": [True, False],
        "with_imaging": [True, False],
        "with_strict_mode": [True, False],
        "with_commandline_tools": [True, False],
        #"with_embree": [True, False],
        #"with_openimageio": [True, False],
        #"with_opencolorio": [True, False],
        "with_usd_imaging": [True, False],
        "with_alembic": [True, False],
        "with_draco": [True, False],  # todo not working on Windows with Monolithic builds
        #"with_ptex": [True, False],
        #"with_openvdb": [True, False],
        "with_safety_over_speed": [True, False],
        "with_metal": [True, False],
        "with_vulkan": [True, False],
        "with_opengl": [True, False],
        "with_monolithic": [True, False],
    }

    default_options = {
        "opensubdiv:with_opengl": True,  # todo this is needed if OpenGL support is true
        "shared": True,
        "with_imaging": True,
        "with_strict_mode": False,
        "with_commandline_tools": True,
        #"with_embree": False,
        #"with_openimageio": False, # todo should be false if imaging is turned off
        #"with_opencolorio": False, # todo check later, todo should be false if imaging is turned off
        "with_usd_imaging": True,
        "with_alembic": True,
        "with_draco": True,
        #"with_ptex": False, # todo check later, todo should be false if imaging is turned off
        #"with_openvdb": False, # todo check later, # todo should be false if imaging is turned off
        "with_safety_over_speed": True,
        "with_metal": True,
        "with_vulkan": False,
        "with_opengl": True,
        "with_monolithic": False,
    }

    short_paths = True
    generators = "cmake"

    requires = ("boost/1.76.0", "onetbb/2020.3","zlib/1.2.12","zstd/1.5.2")# Note: USD does not depend on zlib and zstd directly, but they are conflicts in the dependency graph...

    @property
    def _source_subfolder(self):
        return "source_subfolder"

    @property
    def _build_subfolder(self):
        return "build_subfolder"

    @property
    def _minimum_cpp_standard(self):
        return 14

    @property
    def _minimum_compilers_version(self):
        return {
            "Visual Studio": "15",
            "gcc": "5",
            "clang": "11",
            "apple-clang": "11.0",
        }

    def export_sources(self):
        self.copy("CMakeLists.txt")

    def config_options(self):
        if self.settings.os != "Macos":
            del self.options.with_metal

    def requirements(self):
        #if self.options.with_embree:
        #    self.requires("embree3/3.13.3@")
        #if self.options.with_openimageio:
        #    self.requires("openimageio/2.3.7.2@")
        #if self.options.with_opencolorio:
        #    self.requires("opencolorio/2.1.0@")
        if self.options.with_alembic:
            self.requires("alembic/1.8.3@")
        if self.options.with_draco:
            self.requires("draco/1.5.3@")
        #if self.options.with_ptex:
        #    self.requires("ptex/2.4.0@")
        #if self.options.with_openvdb:
        #    self.requires("openvdb/8.0.1@")
        if self.options.with_imaging:
            self.requires("opensubdiv/3.4.4@")

    def validate(self):
        if self.settings.compiler.get_safe("cppstd"):
            tools.check_min_cppstd(self, self._minimum_cpp_standard)
        min_version = self._minimum_compilers_version.get(str(self.settings.compiler))
        if not min_version:
            self.output.warn("{} recipe lacks information about the {} compiler support.".format(self.name, self.settings.compiler))
        else:
            if tools.Version(self.settings.compiler.version) < min_version:
                raise ConanInvalidConfiguration(
                    "{} requires C++{} support. The current compiler {} {} does not support it.".format(self.name, self._minimum_cpp_standard, self.settings.compiler, self.settings.compiler.version)
                )

        # todo cant build usd_imaging if imaging is off
        # todo embree can't be build if PXR_BUILD_IMAGING is off

    def source(self):
        get(self, **self.conan_data["sources"][self.version], strip_root=True, destination=self._source_subfolder)

    @functools.lru_cache(1)
    def _configure_cmake(self):
        cmake = CMake(self)
        cmake.definitions["PXR_STRICT_BUILD_MODE"] = self.options.with_strict_mode
        cmake.definitions["PXR_VALIDATE_GENERATED_CODE"] = False
        cmake.definitions["PXR_BUILD_TESTS"] = False
        cmake.definitions["PXR_BUILD_EXAMPLES"] = False
        cmake.definitions["PXR_BUILD_TUTORIALS"] = False
        cmake.definitions["PXR_ENABLE_PYTHON_SUPPORT"] = False
        cmake.definitions["PXR_BUILD_USD_TOOLS"] = self.options.with_commandline_tools
        cmake.definitions["PXR_BUILD_IMAGING"] = self.options.with_imaging
        cmake.definitions["PXR_BUILD_USDVIEW"] = False
        #cmake.definitions["PXR_BUILD_EMBREE_PLUGIN"] = self.options.with_embree
        #cmake.definitions["PXR_BUILD_OPENIMAGEIO_PLUGIN"] = self.options.with_openimageio
        #cmake.definitions["PXR_BUILD_OPENCOLORIO_PLUGIN"] = self.options.with_opencolorio
        cmake.definitions["PXR_BUILD_USD_IMAGING"] = self.options.with_usd_imaging
        cmake.definitions["PXR_BUILD_ALEMBIC_PLUGIN"] = self.options.with_alembic
        cmake.definitions["PXR_BUILD_DRACO_PLUGIN"] = self.options.with_draco
        # todo check if needed when building alembic with HDF5
        cmake.definitions["PXR_ENABLE_HDF5_SUPPORT"] = self.options["alembic"].with_hdf5
        cmake.definitions["PXR_ENABLE_PTEX_SUPPORT"] = False #self.options.with_ptex
        #cmake.definitions["PXR_ENABLE_OPENVDB_SUPPORT"] = self.options.with_openvdb
        cmake.definitions["PXR_BUILD_MONOLITHIC"] = self.options.with_monolithic
        cmake.definitions["PXR_PREFER_SAFETY_OVER_SPEED"] = self.options.with_safety_over_speed
        cmake.definitions["PXR_ENABLE_METAL_SUPPORT"] = self.options.get_safe("with_metal", default=False)
        cmake.definitions["PXR_ENABLE_VULKAN_SUPPORT"] = self.options.with_vulkan
        cmake.definitions["PXR_ENABLE_OPENGL_SUPPORT"] = self.options.with_opengl
        cmake.configure(build_folder=self._build_subfolder)

        return cmake

    def build(self):
        paths = [
            os.path.join(self._source_subfolder, "CMakeLists.txt"),
            os.path.join(self._source_subfolder, "cmake", "macros", "Public.cmake"),
            os.path.join(self._source_subfolder, "cmake", "macros", "Private.cmake"),
        ]
        for path in paths:
            replace_in_file(self, path, "${CMAKE_SOURCE_DIR}", "${CMAKE_SOURCE_DIR}/source_subfolder")

        replace_in_file(self, os.path.join(self._source_subfolder, "cmake","modules","FindOpenVDB.cmake"), """find_library( OPENVDB_LIBRARY
    NAMES
        openvdb""", """find_library( OPENVDB_LIBRARY
    NAMES
        libopenvdb""")

        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        self.copy("LICENSE.txt", dst="licenses", src=self._source_subfolder)
        cmake = self._configure_cmake()
        cmake.install()

    # todo do this
    """def package_info(self): 
        self.cpp_info.set_property("cmake_file_name", "USD")

        self.cpp_info.names["cmake_find_package"] = "USD"
        self.cpp_info.names["cmake_find_package_multi"] = "USD"

        self.cpp_info.components["osdcpu"].libs = ["osdCPU"]
        self.cpp_info.components["osdcpu"].set_property("cmake_target_name", "OpenSubdiv::osdcpu")

        if self.options.with_tbb:
            self.cpp_info.components["osdcpu"].requires = ["onetbb::onetbb"]

        if self._osd_gpu_enabled:
            self.cpp_info.components["osdgpu"].libs = ["osdGPU"]
            self.cpp_info.components["osdgpu"].set_property("cmake_target_name", "OpenSubdiv::osdgpu")
            dl_required = self.options.with_opengl or self.options.with_opencl
            if self.settings.os in ["Linux", "FreeBSD"] and dl_required:
                self.cpp_info.components["osdgpu"].system_libs = ["dl"]"""

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