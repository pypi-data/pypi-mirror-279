import glob
import imp
import setuptools
import sys
import unittest
import os
import shutil


class UseUnitTest(unittest.TestCase):
    def runTest(self):
        self.fail(
            "Running tests with setup.py is not supported because it installs "
            "dependencies incorrectly. Please use unittest directly instead."
        )


def gtirb_test_suite():
    test_suite = unittest.TestSuite()
    test_suite.addTest(UseUnitTest())
    return test_suite


# copy over files needed for sdist: README and LICENCE
root_dir = "/builds/rewriting/gtirb"
this_dir = os.path.dirname(__file__)
shutil.copyfile(os.path.join(root_dir, "README.md"), "README")
shutil.copyfile(os.path.join(root_dir, "LICENSE.txt"), "LICENSE")

# Set the version
version = imp.load_source(
    "pkginfo.version", "gtirb/version.py"
).API_VERSION

# run setuptools
if __name__ == "__main__":
    with open("README", "r") as fh:
        long_description = fh.read().replace(
            ".gtirb.svg",
            "https://raw.githubusercontent.com/"
            "GrammaTech/gtirb/master/.gtirb.svg",
        )

    setuptools.setup(
        name="gtirb",
        version=version,
        author="GrammaTech",
        author_email="gtirb@grammatech.com",
        description="GrammaTech Intermediate Representation for Binaries",
        packages=setuptools.find_packages(),
        package_data={"gtirb": ["py.typed"]},
        test_suite="setup.gtirb_test_suite",
        install_requires=[
            "networkx",
            "protobuf<=3.20.1",
            "intervaltree",
            "sortedcontainers",
            "typing-extensions>=3.7.4.2",
        ],
        extras_require={
            "doc": ["sphinx", "sphinx-autodoc-typehints"],
            "dev": ["mypy==0.961", "mypy-protobuf==3.3.0", "types-protobuf==3.20.4"],
        },
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ],
        python_requires=">=3.6",
        long_description=long_description,
        long_description_content_type="text/markdown",
        url="https://github.com/grammatech/gtirb",
        license="MIT",
    )
