from conan import ConanFile
from conan.tools.files import get, copy
from conan.tools.cmake import CMake, cmake_layout
from conan.errors import ConanInvalidConfiguration
import os
import shutil

class PinmameConan(ConanFile):
    name = "libpinmame"
    description = "Pinball Multiple Arcade Machine Emulator Library"
    url = "https://github.com/conan-io/conan-center-index"
    homepage = "https://github.com/vpinball/pinmame"
    license = "old MAME/BSD"
    topics = ("emulator", "emulation", "pinball", "pinmame" )
    settings = "os", "arch", "compiler", "build_type"
    requires = "zlib/1.2.13"
    generators = "CMakeDeps", "CMakeToolchain"
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

    def source(self):
        get(self, **self.conan_data["sources"][self.version], strip_root=True)

    def build(self):
        if self.settings.os == "iOS":
            cmakelists_txt = "CMakeLists_ios-arm64.txt"
        elif self.settings.os == "Macos":
            cmakelists_txt = "CMakeLists_osx-x64.txt"
        elif self.settings.os == "Android":
            cmakelists_txt = "CMakeLists_android-arm64-v8a.txt"
        elif self.settings.os == "Windows":
            cmakelists_txt = "CMakeLists_win-x64.txt"
        elif self.settings.os == "Linux":
            cmakelists_txt = "CMakeLists_linux-x64.txt"
        else:
            raise ConanInvalidConfiguration("Invalid config")
        shutil.copy(os.path.join(self.folders.source_folder, "cmake", "libpinmame", cmakelists_txt), os.path.join(self.folders.source_folder, "CMakeLists.txt"))
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
