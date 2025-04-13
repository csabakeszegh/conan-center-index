from conan import ConanFile
from conan.errors import ConanInvalidConfiguration
from conan.tools.apple import is_apple_os
from conan.tools.cmake import CMake, CMakeDeps, CMakeToolchain, cmake_layout
from conan.tools.files import apply_conandata_patches, copy, export_conandata_patches, get, replace_in_file, rmdir, save
from conan.tools.microsoft import is_msvc
from conan.tools.scm import Version
import os

required_conan_version = ">=2.0.0"


class SdlttfConan(ConanFile):
    name = "sdl_ttf"
    description = "A TrueType font library for SDL"
    license = "Zlib"
    topics = ("sdl3", "sdl2_ttf", "sdl", "sdl_ttf", "ttf", "font")
    homepage = "https://www.libsdl.org/projects/SDL_ttf"
    url = "https://github.com/conan-io/conan-center-index"

    settings = "os", "arch", "compiler", "build_type"
    options = {
        "shared": [True, False],
        "fPIC": [True, False],
        "with_harfbuzz": [True, False],
    }
    default_options = {
        "shared": False,
        "fPIC": True,
        "with_harfbuzz": False,
    }

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def configure(self):
        if self.options.shared:
            self.options.rm_safe("fPIC")
        self.settings.rm_safe("compiler.cppstd")
        self.settings.rm_safe("compiler.libcxx")
        self.options["sdl"].shared = self.options.shared

    def layout(self):
        cmake_layout(self, src_folder="src")

    def requirements(self):
        self.requires("freetype/2.13.2")
        self.requires("sdl/[>=3.2.6 <4]", transitive_headers=True, transitive_libs=True)
        if self.options.get_safe("with_harfbuzz"):
            self.requires("harfbuzz/8.3.0")

    def validate(self):
        if Version(self.version).major != Version(self.dependencies["sdl"].ref.version).major:
            raise ConanInvalidConfiguration("sdl & sdl_ttf must have the same major version")

        if self.options.shared != self.dependencies["sdl"].options.shared:
            raise ConanInvalidConfiguration("sdl & sdl_ttf must be built with the same 'shared' option value")
        else:
            if is_msvc(self) and self.options.shared:
                raise ConanInvalidConfiguration(f"{self.ref} shared is not supported with Visual Studio")

    def build_requirements(self):
        self.tool_requires("cmake/[>=3.17 <4]")

    def source(self):
        get(self, **self.conan_data["sources"][self.version], strip_root=True)

    def generate(self):
        tc = CMakeToolchain(self)
        tc.variables["SDLTTF_SAMPLES"] = False
        tc.variables["SDLTTF_VENDORED"] = False
        tc.variables["SDLTTF_INSTALL"] = True
        tc.variables["SDLTTF_HARFBUZZ"] = self.options.with_harfbuzz
        tc.variables["SDLTTF_DEBUG_POSTFIX"] = ""
        tc.cache_variables["CMAKE_POLICY_DEFAULT_CMP0077"] = "NEW"
        tc.generate()
        deps = CMakeDeps(self)
        deps.generate()


    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        copy(self, "COPYING.txt", src=self.source_folder, dst=os.path.join(self.package_folder, "licenses"))
        copy(self, "LICENSE.txt", src=self.source_folder, dst=os.path.join(self.package_folder, "licenses"))
        cmake = CMake(self)
        cmake.install()
        rmdir(self, os.path.join(self.package_folder, "cmake"))
        rmdir(self, os.path.join(self.package_folder, "lib", "cmake"))
        rmdir(self, os.path.join(self.package_folder, "lib", "pkgconfig"))
        rmdir(self, os.path.join(self.package_folder, "SDL_ttf.framework"))
        rmdir(self, os.path.join(self.package_folder, "share"))

    def package_info(self):
        suffix = "-shared" if self.options.shared else "-static"

        self.cpp_info.set_property("cmake_file_name", "SDL3_ttf")
        self.cpp_info.set_property("pkg_config_name", "SDL3_ttf")
        self.cpp_info.set_property("cmake_target_name", "SDL3_ttf::SDL3_ttf")

        self.cpp_info.components["_sdl3_ttf"].includedirs.append(os.path.join("include", "SDL3_ttf"))
        self.cpp_info.components["_sdl3_ttf"].libs = ["SDL3_ttf"]
        self.cpp_info.components["_sdl3_ttf"].set_property("cmake_target_name", f"SDL3_ttf::SDL3_ttf{suffix}")
        self.cpp_info.components["_sdl3_ttf"].requires = ["freetype::freetype", "sdl::sdl3"]
        if self.options.get_safe("with_harfbuzz"):
            self.cpp_info.components["_sdl3_ttf"].requires.append("harfbuzz::harfbuzz")
