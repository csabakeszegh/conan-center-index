from conan import ConanFile
from conan.tools.files import get, copy, rmdir
from conan.tools.layout import basic_layout
from conan.tools.gnu import AutotoolsToolchain, AutotoolsDeps, Autotools
import os

class LibSerialPortConan(ConanFile):
    name = "libserialport"
    license = "LGPL-3.0-or-later"
    url = "https://github.com/sigrokproject/libserialport"
    description = "Cross-platform library for accessing serial ports"
    topics = ("serial", "serial-port", "libserialport")
    homepage = "https://github.com/sigrokproject/libserialport"
    settings = "os", "compiler", "build_type", "arch"
    generators = "AutotoolsToolchain", "AutotoolsDeps"
    package_type = "library"
    options = {
        "shared": [True, False],
        "fPIC": [True, False],
    }
    default_options = {
        "shared": False,
        "fPIC": True,
    }

    def layout(self):
        basic_layout(self, src_folder="src")

    def build_requirements(self):
        self.tool_requires("autoconf/2.71")
        self.tool_requires("automake/1.16.5")
        self.tool_requires("libtool/2.4.7")
        self.tool_requires("pkgconf/1.9.5")

    def source(self):
        get(self, **self.conan_data["sources"][self.version], strip_root=True)

    def build(self):
        self.run(f"sh {self.source_folder}/autogen.sh")
        autotools = Autotools(self)
        autotools.configure()
        autotools.make()

    def package(self):
        autotools = Autotools(self)
        autotools.install()
        copy(self, "COPYING", dst=os.path.join(self.package_folder, "licenses"), src=self.source_folder)
        rmdir(self, os.path.join(self.package_folder, "lib", "pkgconfig"))
        rmdir(self, os.path.join(self.package_folder, "lib", "libserialport.la"))
        rmdir(self, os.path.join(self.package_folder, "share"))

    def package_info(self):
        self.cpp_info.libs = ['serialport']
        self.cpp_info.includedirs = ['include'] 