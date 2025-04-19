from conan import ConanFile
from conan.tools.files import get, copy, rm
from conan.tools.cmake import cmake_layout, CMake
from conan.tools.files import apply_conandata_patches, export_conandata_patches
import os

class LibzedmdConan(ConanFile):
    name = "libzedmd"
    license = "GPL-3.0"
    url = "https://github.com/PPUC/libzedmd"
    homepage = "https://github.com/PPUC/libzedmd"
    description = "ZeDMD communication library"
    topics = ("zedmd", "display", "ppuc", "vpx", "virtual pinball")
    settings = "os", "arch", "compiler", "build_type"
    generators = "CMakeToolchain", "CMakeDeps"

    options = {
        "shared": [True, False],
        "with_client": [True, False]
    }
    default_options = {
        "shared": True,
        "with_client": True
    }

    def export_sources(self):
        export_conandata_patches(self)
        copy(self, "CMakeLists.txt", src=os.path.join(self.recipe_folder, "conan"), dst=os.path.join(self.export_sources_folder, "conan"))

    def requirements(self):
        self.requires("miniz/3.0.2")
        self.requires("sockpp/1.0.0")
        self.requires("libserialport/cci.20250418")
        self.requires("komihash/5.25")
        self.requires("libframeutil/cci.20250418")
        if self.options.with_client:
            self.requires("cargs/1.2.0")

    def layout(self):
        cmake_layout(self, src_folder="src")

    def source(self):
        get(self, **self.conan_data["sources"][self.version], strip_root=True, destination=self.source_folder)

    def build(self):
        rm(self, "CMakeLists.txt", self.source_folder)
        copy(self, "CMakeLists.txt", src=os.path.join(self.export_sources_folder, "conan"), dst=self.source_folder)
        apply_conandata_patches(self)
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()
        copy(self, "LICENSE", dst=os.path.join(self.package_folder, "licenses"), src=self.source_folder)

    def package_info(self):
        self.cpp_info.libs = ["zedmd"]
