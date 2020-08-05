from conans import ConanFile, CMake, tools

class EchoConan(ConanFile):
    name = "JMI"
    description = "JNI Modern Interface in C++"
    topics = ("JMI")
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = {"shared": False}
    generators = "cmake"
    #exports_sources = "src/*","CMakeLists.txt"

    def source(self):
        self.run("git clone https://github.com/wang-bin/JMI.git")

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()