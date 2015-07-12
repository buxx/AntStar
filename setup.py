from setuptools import setup, find_packages
import antstar

try:
    import pypandoc
    description = pypandoc.convert('README.md', 'rst')
except (IOError, ImportError):
    print('pypandoc not found')
    description = open('README.md').read()

setup(
    name='antstar',
    version='0.2.1.1',
    packages=find_packages(),
    install_requires=[],
    author='Bastien Sevajol',
    author_email="antstar@bux.fr",
    description='Found path in 2d environment as blind ant',
    long_description=description,
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
