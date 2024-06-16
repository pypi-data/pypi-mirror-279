from setuptools import setup, find_packages

setup(
    name="dinjectorr",
    version="0.1.5",
    packages=find_packages(),
    description="A simple dependency injector for Python",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="DMYTRO IVANOV",
    author_email="dima.ivanov.py@gmail.com",
    url="https://github.com/dmtno/dinjectorr",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
