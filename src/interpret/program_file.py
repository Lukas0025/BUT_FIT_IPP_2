#!/usr/bin/env python3
##
# Project: ipp2
# file with xml file reader
# @author Lukáš Plevač <xpleva07>
# @date 18.4.2021

import xml.etree.ElementTree as ET
import math
import errors

class program_file:
    
    ##
    # Load program file and check headers and sort inst by order
    # @param filename - str name of file
    def __init__(self, filename):
        try:
            self._xml_tree = ET.parse(filename)
        except ET.ParseError as error:
            errors.xml("xml error: {}".format(error))
        except FileNotFoundError as error:
            errors.open_input_file(error)
        except Exception:
            errors.open_input_file("unexpected error")
        
        self._check_header()
        self._sort_tree()

    ##
    # Check if header of program is of IPP21
    def _check_header(self):
        root = self._xml_tree.getroot()

        if (root.tag.lower() != "program"):
            errors.xml_struct("root tag is not program")
        
        if ('language' not in self._get_lower_attrib(root) or self._get_lower_attrib(root)['language'].lower() != 'ippcode21'):
            errors.xml_struct("bad language attribute for root tag")

    ##
    # Get all attributes of element in low case
    # @param el - xml element
    # @return array of arguments
    def _get_lower_attrib(self, el):
        out = {}

        for attrib in el.attrib:
            out[attrib.lower()] = el.attrib[attrib]

        return out

    ##
    # Sort inscrustions tree by order argument
    def _sort_tree(self):

        last_min = -math.inf
        root = self._xml_tree.getroot()

        self._sort_index = []

        for index in range(self.length()):
            local_min = {'value': math.inf, 'index': math.nan}

            for inst in range(self.length()):
                if ('order' not in self._get_lower_attrib(root[inst])):
                    errors.xml_struct("missing order attribute for inscruction")
                
                if root[inst].tag.lower() != "instruction":
                    errors.xml_struct("bad tag {}".format(root[inst].tag))
                
                try:
                    el_order = int(self._get_lower_attrib(root[inst])['order'])
                except ValueError as error:
                    errors.xml_struct("bad order attribute for inscruction: {}".format(error))

                if (el_order < local_min['value'] and el_order > last_min):
                    local_min['value'] = el_order
                    local_min['index'] = inst
                elif el_order == local_min['value']:
                    errors.xml_struct("two or more same orders: {}".format(el_order))

            self._sort_index.append(local_min['index'])
            last_min = local_min['value']
    
    ##
    # Get count of inscritions in program
    # @return int count
    def length(self):
        return len(self._xml_tree.getroot())

    ##
    # Get inscrition el on index (sorted) from 0 to N normalized
    # @param index int index of inscrustion
    # @return xml element
    def get(self, index):
        return self._xml_tree.getroot()[self._sort_index[index]]
