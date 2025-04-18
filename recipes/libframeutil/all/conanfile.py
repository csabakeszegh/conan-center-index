from conan import ConanFile
from conan.tools.files import get, copy
from conan.tools.layout import basic_layout
import os

class LibFrameutilConan(ConanFile):
    name = "libframeutil"
    license = "GPL3"
    url = "https://github.com/ppuc/libframeutil"
    description = "C++ header-only library for working with CAN and LIN frames"
    homepage = "https://github.com/ppuc/libframeutil"
    topics = ("libframeutil", "ppuc", "dmd", "vpx", "virtual pinball", "header-only")
    settings = "os", "arch", "compiler", "build_type"
    no_copy_source = True
    package_type = "header-library"

    def layout(self):
        basic_layout(self, src_folder="src")

    def source(self):
        get(self, **self.conan_data["sources"][self.version], strip_root=True, destination=self.source_folder)

    def package(self):
        copy(self, "*.h", dst=os.path.join(self.package_folder, "include"), src=os.path.join(self.source_folder, "include"))
        copy(self, "LICENSE*", dst=os.path.join(self.package_folder, "licenses"), src=self.source_folder)

    def package_id(self):
        self.info.clear()  # Header-only

    def package_info(self):
        self.cpp_info.includedirs = ["include"]