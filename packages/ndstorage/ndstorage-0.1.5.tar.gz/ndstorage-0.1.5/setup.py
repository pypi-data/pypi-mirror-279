import setuptools
from os import path

with open("README.md", "r") as fh:
    long_description = fh.read()

# extract version
path = path.realpath("ndstorage/_version.py")
version_ns = {}
with open(path, encoding="utf8") as f:
    exec(f.read(), {}, version_ns)
version = version_ns["__version__"]

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setuptools.setup(
    name="ndstorage",
    version=version,
    author="Henry Pinkard",
    author_email="henry.pinkard@gmail.com",
    description="Python libraries for N-dimensional datasets, including NDTiff",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/micro-manager/NDStorage",
    packages=setuptools.find_packages(),
    install_requires=requirements,
    python_requires=">=3.6",
    extras_require={
        "test": [
            "pytest",
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
)
