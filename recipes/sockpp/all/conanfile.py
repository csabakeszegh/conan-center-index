from conan import ConanFile
from conan.tools.files import get, copy, rmdir
from conan.tools.cmake import cmake_layout, CMake, CMakeToolchain
import os

class Sockpp(ConanFile):
    name = "sockpp"
    description = """Modern C++ socket library."""
    license = "BSD-3-Clause License"
    author = "fpagliughi"
    settings = "os", "compiler", "build_type", "arch"
    options = {
        "shared" : [True, False],
        "with_can": [True, False]
    }
    default_options = {
        "shared" : True,
        "with_can": False
    }

    def layout(self):
        cmake_layout(self, src_folder="src")

    def generate(self):
        tc = CMakeToolchain(self)
        if self.options.shared:
            tc.variables["SOCKPP_BUILD_SHARED"] = "ON"
            tc.variables["SOCKPP_BUILD_STATIC"] = "OFF"
        else:
            tc.variables["SOCKPP_BUILD_SHARED"] = "OFF"
            tc.variables["SOCKPP_BUILD_STATIC"] = "ON"

        if self.options.with_can:
            tc.variables["SOCKPP_BUILD_CAN"] = "ON"
        tc.variables["SOCKPP_BUILD_EXAMPLES"] = "OFF"
        tc.variables["SOCKPP_BUILD_TESTS"] = "OFF"
        tc.variables["SOCKPP_BUILD_DOCUMENTATION"] = "OFF"
        tc.generate()

    def source(self):
        get(self, **self.conan_data["sources"][self.version], strip_root=True)

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        copy(self, "LICENSE", self.source_folder, os.path.join(self.package_folder, "licenses"))
        cmake = CMake(self)
        cmake.install()
        rmdir(self, os.path.join(self.package_folder, "lib", "cmake"))

    def package_info(self):
        self.cpp_info.includedirs = ["include"]
        self.cpp_info.libdirs = ["lib"]
        if self.settings.os == "Windows":
            self.cpp_info.libs = ["sockpp-static"]
            self.cpp_info.system_libs = ["ws2_32"]
        if self.settings.os == "Linux":
            self.cpp_info.libs = ["sockpp"]