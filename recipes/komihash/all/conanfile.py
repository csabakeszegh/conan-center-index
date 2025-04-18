from conan import ConanFile
from conan.tools.files import get, copy
from conan.tools.layout import basic_layout
import os

class KomihashConan(ConanFile):
    name = "komihash"
    license = "MIT License"
    url = "https://github.com/avaneev/komihash"
    description = "Fast, portable, and high-quality hash functions"
    topics = ("hash", "hashing", "header-only", "komihash")
    homepage = "https://github.com/avaneev/komihash"
    settings = "os", "arch", "compiler", "build_type"
    no_copy_source = True
    package_type = "header-library"

    def layout(self):
        basic_layout(self, src_folder="src")

    def source(self):
        get(self, **self.conan_data["sources"][self.version], strip_root=True, destination=self.source_folder)

    def package(self):
        copy(self, "*.h", src=self.source_folder, dst=os.path.join(self.package_folder, "include"))
        copy(self, "LICENSE*", dst=os.path.join(self.package_folder, "licenses"), src=self.source_folder)

    def package_id(self):
        self.info.clear()  # header-only

    def package_info(self):
        self.cpp_info.includedirs = ["include"]
