from setuptools import setup, Extension
import pybind11
from pybind11.setup_helpers import Pybind11Extension, build_ext

setup(
    name="pyunwrap",
    version = "0.0.1",
    ext_modules = [Pybind11Extension("pyunwrap",["unwrap.cpp"],),],
    cmdclass = {"build_ext": build_ext},
)

