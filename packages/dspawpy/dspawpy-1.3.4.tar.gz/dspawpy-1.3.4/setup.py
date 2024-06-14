# -*- coding: utf-8 -*-
import os
from setuptools import find_packages, setup


def read(fname):
    with open(
        os.path.join(os.path.abspath(os.path.dirname(__file__)), fname),
        "r",
        encoding="utf-8",
    ) as fin:
        return fin.read()


setup(
    name="dspawpy",
    version="1.3.4",
    packages=find_packages(),
    url="http://www.hzwtech.com/",
    license="MIT",
    author="Hzwtech",
    author_email="ZhengZhilin@hzwtech.com",
    description="Tools for dspaw",
    install_requires=[
        "pymatgen",
        "statsmodels",
        "h5py",  # parse h5
        "prompt_toolkit",  # cli completer
        "loguru",  # log
        "polars>=0.18",  # speed up pandas, write_csv starts from 0.18
        "ruamel.yaml",  # ordered yaml
    ],
    python_requires=">=3.8",
    entry_points={"console_scripts": ["cli=dspawpy.cli.cli:main"]},
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    license_files=("LICENSE.txt",),
)
