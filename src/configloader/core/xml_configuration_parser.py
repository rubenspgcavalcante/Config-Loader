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

import re
from xml.etree import ElementTree
from xml.etree.ElementTree import Element
from types_parser import TypeParser
from dict_struct import DictStruct

class XMLTemplateError(StandardError):
    def __init__(self, msg):
        StandardError.__init__(self, msg)

class XMLConfigurationParser(object):
    def __init__(self):
        self.typeParser = TypeParser()

    def clean(self, text):
        if text is not None:
            return text.replace("\n", "").replace("\t", "")
        else:
            return ""

    def parseTupleOrListTag(self, element, structure, type):
        """
        Parses a tag of type 'tuple' or 'list' and analyse the content type
        of this structure
        e.g.:
            <tag type="tuple(int)">"20", "10"</tag>
            <tag type="tuple(float)">"20.3", "10.1"</tag>
            <tag type="list(str)">"hello", "world"</tag>

        :type element: Element
        :param element: The element tree which contains the tag
        :rtype : tuple|list
        """
        if structure == "tuple":
            return self.typeParser.tuple(element.text, type)

        if structure == "list":
            return self.typeParser.list(element.text, type)


    def processType(self, element):
        """
        Process a value using the default cast, referenced by the type
        attribute into the tag
        e.g.:
            <tag type="int">20</tag>
            <tag type="float">1.9</tag>

        :type element: Element
        :param element: The tag to covert
        """
        match = re.match(r'(?P<struct>tuple|list)\((?P<type>.*)\)', element.attrib["type"])
        if match:
            processed = self.parseTupleOrListTag(element, match.group('struct'), match.group('type') )

        elif element.attrib["type"] == "int":
            processed = self.typeParser.int(element.text)

        elif element.attrib["type"] == "float":
            processed = self.typeParser.float(element.text)

        elif element.attrib["type"] == "bool":
            processed = self.typeParser.bool(element.text)

        else:
            processed = element.text

        return processed

    def XMLToDict(self, parent_element, template_args=None):
        """
        Parse a XML etree object into a dict, recursively

        :type parent_element: Element
        :param parent_element: The parent element to serve as the wrapper of the dict

        :type template_args: dict
        :param template_args: Template arguments to process the tags with the 'template' attribute
        :returns The parsed dict
        """
        result = dict()
        for element in parent_element:
            if len(element):
                obj = self.XMLToDict(element, template_args)
            else:
                obj = self.clean(element.text)

            if result.get(element.tag):
                if hasattr(result[element.tag], "append"):
                    result[element.tag].append(obj)
                else:
                    result[element.tag] = [result[element.tag], obj]
            else:
                if 'type' in element.attrib:
                    obj = self.processType(element)

                if 'template' in element.attrib:
                    if element.attrib['template'] == 'true' and template_args != None:
                        try:
                            obj = element.text.format(**template_args)

                        except KeyError as e:
                            raise XMLTemplateError("Template parse error. Missing argument %s" % e.args)

                result[element.tag] = obj
        return result

    def parse(self, filePath, **variables):
        """
        Parse a file and loads it into a structured format

        :type filePath: str
        :param filePath: The path to the XML configuration file

        :type variables: dict
        :param variables: The template variables to substitute in the xml file

        :rtype : DictStruct
        """
        xml = None
        with open(filePath, 'rt') as confFile:
            xml = ElementTree.parse(confFile)

        confDict = self.XMLToDict(xml._root, variables)
        return DictStruct(**confDict)