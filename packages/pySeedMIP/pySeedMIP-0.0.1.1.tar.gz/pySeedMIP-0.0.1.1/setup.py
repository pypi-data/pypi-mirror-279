from setuptools import setup, Extension, find_packages

setup(
    name="pySeedMIP",
    version="0.0.1.1",
    aduthor="Seed",
    description="SeedMIP for python",
    packages=find_packages(),   # automatically find all python packages
    package_data={'pySeedMIP': ['pySeedMIP.cpython-39-x86_64-linux-gnu.so']},
)
