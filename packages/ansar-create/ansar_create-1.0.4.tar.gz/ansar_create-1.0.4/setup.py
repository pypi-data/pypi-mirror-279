# Standard PyPi packaging.
# Build materials and push to pypi.org.
# Author: Scott Woods <scott.18.ansar@gmail.com>
import sys
import os
import setuptools
import re

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.rst')) as f:
    README = f.read()

#
#
VERSION_PATTERN = re.compile(r'([0-9]+)\.([0-9]+)\.([0-9]+)')

#
#
with open(os.path.join(here, 'PACKAGE')) as f:
    p = f.read()
PACKAGE = p[:-1]

#
#
with open(os.path.join(here, 'DESCRIPTION')) as f:
    d = f.read()
DESCRIPTION = d[:-1]

#
#
with open(os.path.join(here, 'VERSION')) as f:
    line = [t for t in f]
VERSION = line[-1][:-1]

if not VERSION_PATTERN.match(VERSION):
    print('Version "%s" does not meet semantic requirements' % (VERSION,))
    sys.exit(1)

with open("DOC_LATEST_LINK", "r", encoding="utf-8") as f:
    d = f.read()
DOC_LINK = d[:-1]

REQUIRES = [
    "ansar-encode>=1.0.2",
]

setuptools.setup(
    name=PACKAGE,
    version=VERSION,
    author="Scott Woods",
    author_email="ansar.library.management@gmail.com",
    description=DESCRIPTION,
    long_description=README,
    #long_description_content_type="text/markdown",
    #project_urls={
    #    "Documentation": DOC_LINK,
    #},
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Linux",
        "Operating System :: macOS",
        "Topic :: Software Development :: Libraries",
    ],
    package_dir={
        "": "src",
    },
    # First folder under "where" defines the name of the
    # namespace. Folders under that (with __init__.py files)
    # define import packages under that namespace.
    packages=setuptools.find_namespace_packages(
        where="src",
    ),
    entry_points = {
        'console_scripts': [
            'ansar=ansar.command.ansar_command:main',
            'ansar-group=ansar.command.ansar_group:main',
        ],
    },
    #python_requires=">=3.6",
    #install_requires=REQUIRES,
)
