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
import cgi
from threading import Lock

__author__ = "Rubens Pinheiro Gonçalves Cavalcante"
__date__ = "08/05/13 19:18"
__licence__ = "GPLv3"
__email__ = "rubenspgcavalcante@gmail.com"

from core.xml_configuration_parser import XMLConfigurationParser
from core.singleton import singleton

@singleton
class Config(object):
    def __init__(self, configFile="config.xml", templates=None):
        self.configFile = configFile
        self._LOCK = Lock()
        self._parser = XMLConfigurationParser()
        if templates is None:
            self._attr = self._parser.parse(configFile)
        else:
            self._attr = self._parser.parse(configFile, **templates)
        self._bck = self._attr

    @property
    def attr(self):
        return self._attr

    @attr.setter
    def attr(self, value):
        value = cgi.escape(value)
        with self._LOCK:
            self._attr = value

    @attr.getter
    def attr(self, value):
        with self._LOCK:
            return self._attr

    @property
    def bck(self):
        return None

    @bck.setter
    def bck(self, value):
        pass

    def reset(self):
        """
        Resets the config object to the default state, based on config,xml
        """
        self._attr = self._bck

    def reload(self):
        """
        Force the reload of the config.xml file
        """
        self._attr = self._parser.parse(self.configFile)
        self._bck = self._attr