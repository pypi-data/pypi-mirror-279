from setuptools import setup, Extension
import os
import pybind11

libpastel_path = "/Users/alexey/Work/Pastel/pastel-lite/libpastel.a"
include_path = "/Users/alexey/Work/Pastel/pastel-lite/lib/include"
secp256k1_include_path = "/Users/alexey/Work/Pastel/pastel-lite/build-native-debug/_deps/libsecp256k1-src/include"
secp256k1_lib_path = "/Users/alexey/Work/Pastel/pastel-lite/build-native-debug/_deps/libsecp256k1-build/src"

botan_include_path = "/Users/alexey/Work/Pastel/pastel-lite/build-native-debug/libbotan-lib/include/botan-3"
botan_lib_path = "/Users/alexey/Work/Pastel/pastel-lite/build-native-debug/libbotan-lib/lib"

fmt_include_path = "/Users/alexey/Work/Pastel/pastel-lite/build-native-debug/_deps/fmt-src/include"
fmt_lib_path = "/Users/alexey/Work/Pastel/pastel-lite/build-native-debug/_deps/fmt-build"
zstd_include_path = "/Users/alexey/Work/Pastel/pastel-lite/build-native-debug/vcpkg_installed/x64-osx/include"
zstd_lib_path = "/Users/alexey/Work/Pastel/pastel-lite/build-native-debug/vcpkg_installed/x64-osx/lib"

required_libs = {
    "libpastel.a": libpastel_path,
    "libsecp256k1.a": os.path.join(secp256k1_lib_path, "libsecp256k1.a"),
    "libbotan-3.a": os.path.join(botan_lib_path, "libbotan-3.a"),
    "libfmt.a": os.path.join(fmt_lib_path, "libfmtd.a"),
    "libzstd.a": os.path.join(zstd_lib_path, "libzstd.a"),
}

for lib_name, lib_path in required_libs.items():
    if not os.path.exists(lib_path):
        raise FileNotFoundError(f"{lib_name} not found. Ensure it is built and located at {lib_path}")

ext_modules = [
    Extension(
        "libpastelid",
        ["pybind_wrapper.cpp"],
        include_dirs=[
            include_path,
            pybind11.get_include(),
            pybind11.get_include(user=True),
            secp256k1_include_path,
            fmt_include_path,
            zstd_include_path,
            botan_include_path,
        ],
        libraries=["pastel", "sodium", "secp256k1", "botan-3", "zstd", "fmtd"],
        library_dirs=[
            os.path.dirname(libpastel_path),
            secp256k1_lib_path,
            zstd_lib_path,
            fmt_lib_path,
            botan_lib_path,
        ],
        language="c++",
        extra_compile_args=["-std=c++20"],
        extra_link_args=["-Wl,-rpath,../"]
    ),
]

setup(
    name="libpastelid",
    version="0.2",
    description="Python bindings for the libpastelid C++ library - PastelID signer/verifier",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author_email="alexey@pastel.network",
    ext_modules=ext_modules,
    zip_safe=False,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
