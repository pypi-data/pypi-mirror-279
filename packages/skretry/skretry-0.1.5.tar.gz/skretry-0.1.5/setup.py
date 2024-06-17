from setuptools import find_packages, setup

setup(
    packages=find_packages(exclude=["tests"]),
    install_requires=['loguru'],
)
