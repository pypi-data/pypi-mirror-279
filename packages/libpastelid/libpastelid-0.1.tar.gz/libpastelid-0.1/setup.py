from setuptools import setup, Extension
import os
import pybind11

pastel_lib_dir = "/Users/alexey/Work/Pastel/pastel-lite/"

# Resolve the absolute paths
libpastel_path = os.path.abspath(os.path.join(pastel_lib_dir, "libpastel.a"))
include_path = os.path.abspath(os.path.join(pastel_lib_dir, "lib/include"))
print(libpastel_path)
print(include_path)

if not os.path.exists(libpastel_path):
    raise FileNotFoundError(f"libpastel.a not found. Ensure it is built and located at {libpastel_path}")

ext_modules = [
    Extension(
        "libpastelid",
        ["pybind_wrapper.cpp"],
        include_dirs=[
            include_path,
            pybind11.get_include(),
            pybind11.get_include(user=True)
        ],
        libraries=["pastel"],
        library_dirs=[os.path.dirname(libpastel_path)],
        language="c++",
        extra_compile_args=["-std=c++20"],
        extra_link_args=["-Wl,-rpath,../"]
    ),
]

setup(
    name="libpastelid",
    version="0.1",
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
