# vim: ts=4:sts=4:sw=4                                                          
#                                                                               
# @author <lucile.gaultier@oceandatalab.com>                                    
# @date 2024-01-10                                                              
#                                                                               
# Copyright (C) 2020-2024 OceanDataLab                                          
#                                                                               
# This program is free software: you can redistribute it and/or modify          
# it under the terms of the GNU Lesser General Public License as                
# published by the Free Software Foundation, either version 3 of the            
# License, or (at your option) any later version.                               
#                                                                               
# This program is distributed in the hope that it will be useful,               
# but WITHOUT ANY WARRANTY; without even the implied warranty of                
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the                 
# GNU Affero General Public License for more details.                           
#                                                                               
# You should have received a copy of the GNU Lesser General Public License      
# along with this program.  If not, see <https://www.gnu.org/licenses/>.        

"""This module provides methods to run command line and validate velocity       
   products                                                                     
                                                                                
"""

import argparse
import logging
import datetime
import os

import odyseamulator_l2.create_l2 as create_l2

# Set up logging                                                                 
logger = logging.getLogger()
logger.handlers = []
handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)
logger.addHandler(handler)
logger.setLevel(logging.WARN)


def run_odyseamulator():
    parser = argparse.ArgumentParser()
    parser.add_argument('parameter_file',
                        type=str, default='',
                        help=f'Python parameter file path'
                        )
    parser.add_argument('--first_cycle',
                        type=int, default=0,
                        help=f'Python parameter file path'
                        )

    parser.add_argument('--last_cycle',
                        type=int, default=2,
                        help=f'Python parameter file path'
                        )
    parser.add_argument('--verbose', action='store_true', default=False,
                        required=False)
    parser.add_argument('--debug', action='store_true', default=False,
                        required=False)
    parser.add_argument('--quiet', action='store_true', default=False,
                        required=False)

    args = parser.parse_args()
    if args.verbose:
        logger.setLevel(logging.INFO)
    if args.debug:
        logger.setLevel(logging.DEBUG)
    if args.quiet:
        logger.setLevel(logging.ERROR)
    create_l2.run(args.parameter_file, args.first_cycle, args.last_cycle)
