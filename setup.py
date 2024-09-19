# Copyright (C) 2023-2024 OceanDataLab                                          
# This file is part of odyseamulator_l2

# this program is free software: you can redistribute it and/or modify          
# it under the terms of the GNU General Public License as published by          
# the Free Software Foundation, either version 3 of the License, or             
# (at your option) any later version.                                           
# this program is distributed in the hope that it will be useful,               
# but WITHOUT ANY WARRANTY; without even the implied warranty of                
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the                 
# GNU General Public License for more details.                                  

# You should have received a copy of the GNU General Public License             
# along with this program.  If not, see <http://www.gnu.org/licenses/>.         


"""Build and install the odyseamulator_l2 package."""

from distutils.core import setup
from setuptools import setup, find_packages
import os
import sys

import logging

logger = logging.getLogger()
handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

# Check Python version
if sys.version_info < (3, 7):
    logger.error('This package is only available for Python >=3.7')
    sys.exit(1)

__package_name__ = 'odyseamulator_l2'
project_dir = os.path.dirname(__file__)
package_dir = os.path.join(project_dir, __package_name__)
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

cmds = ['odyseamul = {}.cli:run_odyseamulator'.format(__package_name__),
        'backup_orbit = {}.cli:backup_orbit'.format(__package_name__),]

setup(
      name='odyseamulator_l2',
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
      entry_points={'console_scripts': cmds},
      package_data={'odyseamulator-l2': ['orbit_files/*.npz', 'uncertainty_tables/*.npz']}
)
