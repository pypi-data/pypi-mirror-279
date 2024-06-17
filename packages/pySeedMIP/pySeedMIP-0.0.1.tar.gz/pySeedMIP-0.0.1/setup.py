from setuptools import setup, Extension, find_packages

setup(
    name="pySeedMIP",
    version="0.0.1",
    author="Seed",
    description="SeedMIP for python",
    packages=find_packages(),   # automatically find all python packages
    package_data={  # include any necessary data files
        "pySeedMIP": ["*.so"],
    },
    install_requires=[
        # include any python dependencies here
    ],
)
