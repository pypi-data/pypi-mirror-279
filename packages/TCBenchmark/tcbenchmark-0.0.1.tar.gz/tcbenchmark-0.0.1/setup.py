# from setuptools import setup, find_packages

# # Based off of copilot example:
# setup(
#     name="TCBench",
#     version="0.0.1",
#     packages=find_packages(),
#     install_requires=[
#         # List project dependencies here.
#         # "numpy>=1.26.4",
#         # "pandas>=2.2.2",
#         # "xarrray>=2024.5.0",
#         # "dask>=2024.5.2",
#         # "dask_ml>=2024.4.4",
#         # "scikit-learn>=1.5",
#         # # 'matplotlib>=3.8',
#         # "netCDF4>=1.6.5",
#     ],
#     author="Milton S. Gomez",
#     author_email="milton.gomez@unil.ch",
#     description="Python platform and benchmark dataset for data-driven tropical cyclone studies.",
#     long_description=open(
#         "/work/FAC/FGSE/IDYST/tbeucler/default/milton/repos/bench_package/README.md"
#     ).read(),
#     long_description_content_type="text/markdown",
#     url="https://github.com/msgomez06/TCBench_Alpha",
#     classifiers=[
#         # How mature is this project? Common values are
#         #   3 - Alpha
#         #   4 - Beta
#         #   5 - Production/Stable
#         "Development Status :: 3 - Alpha",
#         "Intended Audience :: Atmospheric Scientists, Machine Learning Researchers",
#         "Topic :: Machine Learning :: Tropical Meteorology :: Benchmarking",
#         "License :: MIT License",
#         # Supported Python versions
#         # "Programming Language :: Python :: 3",
#     ],
#     keywords="Meteorological Atmospheric Science Machine Learning Benchmarking Tropical Cyclones",
#     # You can specify the packages manually here if your project is
#     # simple. Or you can use find_packages().
#     # packages=['mypackage'],
#     # Alternatively, if you want to distribute just a my_module.py, uncomment:
#     # py_modules=["my_module"],
# )


# --------------------------------------------------------------------------------
# Scikit learn implementation

#! /usr/bin/env python
#
# Authors: The scikit-learn developers
# License: 3-clause BSD

import importlib
import os
import platform
import shutil
import sys
import traceback
from os.path import join

from setuptools import Command, Extension, setup
from setuptools.command.build_ext import build_ext


DISTNAME = "TCBenchmark"
DESCRIPTION = (
    "Python platform and benchmark dataset for data-driven tropical cyclone studies."
)
with open(
    "/work/FAC/FGSE/IDYST/tbeucler/default/milton/repos/bench_package/README.md"
) as f:
    LONG_DESCRIPTION = f.read()
MAINTAINER = "Milton S. Gomez"
MAINTAINER_EMAIL = "milton.gomez@unil.ch"
URL = "https://wp.unil.ch/dawn/"
# DOWNLOAD_URL = "https://pypi.org/project/scikit-learn/#files"
LICENSE = "MIT"
PROJECT_URLS = {
    "Bug Tracker": "https://github.com/msgomez06/TCBench_Alpha/issues",
    "Documentation": "https://github.com/msgomez06/TCBench_Alpha/wiki",
    "Source Code": "https://github.com/msgomez06/TCBench_Alpha",
}


VERSION = "0.0.1"

# Custom clean command to remove build artifacts


class CleanCommand(Command):
    description = "Remove build artifacts from the source tree"

    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        # Remove c files if we are not within a sdist package
        cwd = os.path.abspath(os.path.dirname(__file__))
        remove_c_files = not os.path.exists(os.path.join(cwd, "PKG-INFO"))
        if remove_c_files:
            print("Will remove generated .c files")
        if os.path.exists("build"):
            shutil.rmtree("build")
        for dirpath, dirnames, filenames in os.walk("tcbenchmark"):
            for filename in filenames:
                root, extension = os.path.splitext(filename)

                if extension in [".so", ".pyd", ".dll", ".pyc"]:
                    os.unlink(os.path.join(dirpath, filename))

                if remove_c_files and extension in [".c", ".cpp"]:
                    pyx_file = str.replace(filename, extension, ".pyx")
                    if os.path.exists(os.path.join(dirpath, pyx_file)):
                        os.unlink(os.path.join(dirpath, filename))

                if remove_c_files and extension == ".tp":
                    if os.path.exists(os.path.join(dirpath, root)):
                        os.unlink(os.path.join(dirpath, root))

            for dirname in dirnames:
                if dirname == "__pycache__":
                    shutil.rmtree(os.path.join(dirpath, dirname))


cmdclass = {
    "clean": CleanCommand,
}


def setup_package():
    python_requires = ">=3.9"
    required_python_version = (3, 9)

    metadata = dict(
        name=DISTNAME,
        maintainer=MAINTAINER,
        maintainer_email=MAINTAINER_EMAIL,
        description=DESCRIPTION,
        license=LICENSE,
        url=URL,
        project_urls=PROJECT_URLS,
        version=VERSION,
        long_description=LONG_DESCRIPTION,
        classifiers=[
            "Intended Audience :: Science/Research",
            "Intended Audience :: Developers",
            "Intended Audience :: Education",
            "License :: OSI Approved :: MIT License",
            "Programming Language :: Python",
            "Topic :: Scientific/Engineering :: Atmospheric Science",
            "Topic :: Scientific/Engineering :: Artificial Intelligence",
            "Development Status :: 3 - Alpha",
            "Operating System :: Microsoft :: Windows",
            "Operating System :: Unix",
            "Operating System :: MacOS",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.9",
            "Programming Language :: Python :: 3.10",
            "Programming Language :: Python :: 3.11",
            "Programming Language :: Python :: 3.12",
        ],
        cmdclass=cmdclass,
        python_requires=python_requires,
        # install_requires=min_deps.tag_to_packages["install"],
        package_data={
            "": ["*.csv", "*.gz", "*.txt", "*.pxd", "*.rst", "*.jpg", "*.css"]
        },
        zip_safe=False,  # the package can run out of an .egg file
        # extras_require={
        #     key: min_deps.tag_to_packages[key]
        #     for key in ["examples", "docs", "tests", "benchmark"]
        # },
    )

    commands = [arg for arg in sys.argv[1:] if not arg.startswith("-")]
    if not all(
        command in ("egg_info", "dist_info", "clean", "check") for command in commands
    ):
        if sys.version_info < required_python_version:
            required_version = "%d.%d" % required_python_version
            raise RuntimeError(
                "Scikit-learn requires Python %s or later. The current"
                " Python version is %s installed in %s."
                % (required_version, platform.python_version(), sys.executable)
            )

    setup(**metadata)


if __name__ == "__main__":
    setup_package()
