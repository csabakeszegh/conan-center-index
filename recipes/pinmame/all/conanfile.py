from conan import ConanFile
from conan.tools.files import get, copy, apply_conandata_patches, export_conandata_patches
from conan.tools.cmake import CMake, cmake_layout, CMakeToolchain
from conan.errors import ConanInvalidConfiguration
import os
import shutil

class PinmameConan(ConanFile):
    name = "pinmame"
    description = "Pinball Multiple Arcade Machine Emulator Library"
    url = "https://github.com/conan-io/conan-center-index"
    homepage = "https://github.com/vpinball/pinmame"
    license = "old MAME/BSD"
    topics = ("emulator", "emulation", "pinball", "pinmame" )
    settings = "os", "arch", "compiler", "build_type"
    generators = "CMakeDeps"
    options = {
        "shared": [True, False],
        "fPIC": [True, False],
    }
    default_options = {
        "shared": True,
        "fPIC": True
    }

    def layout(self):
        cmake_layout(self, src_folder="src")

    def export_sources(self):
        export_conandata_patches(self)

    def source(self):
        get(self, **self.conan_data["sources"][self.version], strip_root=True)

    def generate(self):
        tc = CMakeToolchain(self)
        tc.variables["BUILD_SHARED"] = self.options.shared
        tc.variables["BUILD_STATIC"] = not self.options.shared
        if self.settings.os == "Windows":
            tc.variables["PLATFORM"] = "win"
        if self.settings.os == "Linux":
            tc.variables["PLATFORM"] = "linux"
        if self.settings.os == "iOS":
            if self.settings.sdk == "iphoneos":
                tc.variables["PLATFORM"] = "ios"
            if self.settings.sdk == "iphonesimulator":
                tc.variables["PLATFORM"] = "ios-simulator"
        if self.settings.os == "tvOS":
            tc.variables["PLATFORM"] = "tvos"
        if self.settings.os == "Android":
            tc.variables["PLATFORM"] = "android"
        if self.settings.os == "Macos":
            tc.variables["PLATFORM"] = "macos"

        if self.settings.arch == "x86_64":
            tc.variables["ARCH"] = "x64"
        if self.settings.arch == "armv8":
            tc.variables["ARCH"] = "arm64"

        tc.generate()

    def build(self):
        cmakelists_txt = os.path.join(self.folders.source_folder, "CMakeLists.txt")
        apply_conandata_patches(self)
        shutil.copy(os.path.join(self.folders.source_folder, "cmake", "libpinmame", "CMakeLists.txt"), cmakelists_txt)
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        copy(self, "LICENSE", src=self.source_folder, dst=os.path.join(self.package_folder, "licenses"))
        copy(self, "libpinmame.h", src=os.path.join(self.source_folder, "src", "libpinmame"), dst=os.path.join(self.package_folder, "include"))
        copy(self, "*.dylib", src=self.build_folder, dst=os.path.join(self.package_folder, "lib"))
        copy(self, "*.a", src=self.build_folder, dst=os.path.join(self.package_folder, "lib"))
        copy(self, "*.lib", src=self.build_folder, dst=os.path.join(self.package_folder, "lib"))
        copy(self, "*.dll", src=self.build_folder, dst=os.path.join(self.package_folder, "lib"))
        copy(self, "*.so*", src=self.build_folder, dst=os.path.join(self.package_folder, "lib"))

    def package_info(self):
        self.cpp_info.set_property("cmake_file_name", "libpinmame")
        self.cpp_info.set_property("cmake_target_name", "libpinmame::libpinmame")
        self.cpp_info.libs = ["pinmame"]
        self.cpp_info.system_libs.append("pthread")
