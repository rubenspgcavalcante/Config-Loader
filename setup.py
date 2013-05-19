#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License version 3 as
published by the Free Software Foundation.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
"""
__author__ = "Rubens Pinheiro Gonçalves Cavalcante"
__date__ = "08/05/13 19:18"
__licence__ = "GPLv3"
__email__ = "rubenspgcavalcante@gmail.com"

from distutils.core import setup

setup(
    name='ConfigLoader',
    version='1.0',
    license="GPLv3",
    description='A xml parser to a config structure',
    author='Rubens Pinheiro Gonçalves Cavalcante',
    author_email='rubenspgcavalcante@gmail.com',
    url="https://github.com/rubenspgcavalcante/Config-Loader",
    package_dir={'configloader': 'src/configloader'},
    package_data={'configloader': ['sample.xml']},
    packages=['configloader', 'configloader.core'],
)
