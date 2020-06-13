from conans import ConanFile, CMake, tools
import os


class QrCodeGeneratorConan(ConanFile):
    name = "qr-code-generator"
    url = "https://github.com/conan-io/conan-center-index"
    homepage = "https://github.com/nayuki/QR-Code-generator"
    description = "High-quality QR Code generator library in Java, JavaScript, Python, C++, C, Rust, TypeScript."
    topics = ["qr-code", "qr-generator", "c-plus-plus"]
    license = "MIT"
    settings = "os", "compiler", "arch", "build_type"
    options = {"shared": [True, False],
               "fPIC": [True, False]}
    default_options = {'shared': False,
                       'fPIC': True}
    exports_sources = ["CMakeLists.txt", "patches/**"]
    generators = "cmake"

    _cmake = None

    @property
    def _source_subfolder(self):
        return "source_subfolder"

    def configure(self):
        if self.settings.compiler == "Visual Studio":
            del self.options.fPIC

    def source(self):
        tools.get(**self.conan_data["sources"][self.version])
        os.rename("QR-Code-generator-{}".format(self.version),
                  self._source_subfolder)

    def _configure_cmake(self):
        if self._cmake:
            return self._cmake
        self._cmake = CMake(self)
        self._cmake.configure()
        return self._cmake

    def _patch_sources(self):
        try:
            for patch in self.conan_data["patches"][self.version]:
                tools.patch(**patch)
        except KeyError:
            pass

    def build(self):
        self._patch_sources()
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        self.copy("Readme.markdown", dst="licenses",
                  src=self._source_subfolder)
        cmake = self._configure_cmake()
        cmake.install()

    def package_info(self):
        self.cpp_info.libs.append("qrcodegen")
