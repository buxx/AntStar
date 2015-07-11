from setuptools import setup, find_packages
import synergine_xyz

setup(
    name='antstar',
    version='0.2',
    packages=find_packages(),
    install_requires=[],
    author='Bastien Sevajol',
    author_email="antstar@bux.fr",
    description='Found path in 2d environment as blind ant',
    long_description=open('README.md').read(),
    include_package_data=True,
    url='https://github.com/buxx/AntStar',
    # https://pypi.python.org/pypi?%3Aaction=list_classifiers.
    classifiers=[
        "Programming Language :: Python",
        "Development Status :: 3 - Alpha",
        "Natural Language :: French",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.4",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)"
    ]
)
