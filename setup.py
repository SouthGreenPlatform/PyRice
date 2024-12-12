from setuptools import setup

with open('README.md','r') as fh:
    long_description = fh.read()

setup(
    name = 'pyrice',
    version = '0.2.13',
    description = 'PyRice: a Python package for functional analysis of rice genes',
    py_modules =['multi_query','utils','build_dictionary'],
    license = 'MIT',
    classifiers = [
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    install_requires=[
        "selenium"
    ],
    packages=["pyrice"],
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://github.com/SouthGreenPlatform/PyRice",
    author = "Pierre Larmande, Quan Do",
    author_email = "pierre.larmande@ird.fr, dohongquan1612@gmail.com",
    include_package_data = True
)
