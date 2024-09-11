#!/usr/bin/env python

from distutils.core import setup
from setuptools import setup, find_packages
import os
import sys

# Check Python version
if not 3 == sys.version_info[0]:
    print('This package is only available for Python 3.x')
    sys.exit(1)

__package_name__ = 'odyseamulator-l2'
project_dir = os.path.dirname(__file__)
package_dir = os.path.join(project_dir, 'odysim')
init_file = os.path.join(package_dir, '__init__.py')

# - Read in the package version and author fields from the Python
#  main __init__.py file:
metadata = {}
with open(init_file, 'rt') as f:
    exec(f.read(), metadata)

requirements = []
with open('requirements.txt', 'r') as f:
    lines = [x.strip() for x in f if 0 < len(x.strip())]
    requirements = [x for x in lines if x[0].isalpha()]
cmds = ['odyseamul = {}.cli: run_odyseamulator'.format(__package_name__),]
setup(
      name='odyseamulator-l2',
      version=metadata['__version__'],
    #package_dir={'odysea-simulator': 'odysim'},
    #packages=[
    #    'odysim'],
      description=metadata['__description__'],
      author=metadata['__author__'],
      author_email=metadata['__author_email__'],
      url=metadata['__url__'],
      keywords=metadata['__keywords__'],
      packages=find_packages(),
      install_requires=requirements,
      setup_require=(),
      package_data={'odyseamulator': ['orbit_files/*.npz', 'uncertainty_tables/*.npz']}
)
