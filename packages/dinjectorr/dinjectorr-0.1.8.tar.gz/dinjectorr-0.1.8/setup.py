from setuptools import setup, find_packages

setup(
    name="dinjectorr",
    version="0.1.8",
    packages=find_packages(),
    url="https://github.com/dmtno/dinjectorr",
    license="MIT",
    author="DMYTRO IVANOV",
    author_email="dima.ivanov.py@gmail.com",
    description="A simple dependency injector for Python",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
)
