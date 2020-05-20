import codecs
import os
from setuptools import find_packages, setup
PACKAGE_NAME = "tx-easgui"
VERSION = "0.1.0"
AUTHOR = "Jose Amoroso"
AUTHOR_EMAIL = "jose.amoroso@yachaytech.edu.ec"
DESCRIPTION = "A language for generating simple interfaces with TkInter."
KEYWORDS = "textX DSL python domain specific languages tkinter interface GUI"
LICENSE = "MIT"
setup(
    name=PACKAGE_NAME,
    version=VERSION,
    description=DESCRIPTION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    keywords=KEYWORDS,
    license=LICENSE,
    packages=find_packages(),
    include_package_data=True,
    package_data={"": ["*.tx"]},
    install_requires=["textx_ls_core"],
    entry_points={"textx_languages": ["easgui = tx_easgui:easgui"]},
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],

)