#!/usr/bin/python
# Copyright (C) 2014 Bitergia
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
#
# Authors:
#   Daniel Izquierdo Cortazar <dizquierdo@bitergia.com>
#

from optparse import OptionParser

from ConfigParser import SafeConfigParser

def read_options():
    """ Function to manage user options
    """

    parser = OptionParser(usage="usage: %prog [options]",
                          version="%prog 0.1")
    parser.add_option("-c", "--config-file",
                      action="store",
                      dest="config_file",
                      default="grimoirelib-metadata.conf",
                      help="Config file")
    (opts, args) = parser.parse_args()

    return opts

def read_config_file(config_file_path):
    """ Reads the config file with a specific format and returns
        the correspondant dictionary

        :param config_file_path: path where the config file is found

        :returns: Dictionary with options read from config file
    """

    parser = SafeConfigParser()
    fd = open(config_file_path, "r")
    parser.readfp(fd)
    fd.close()

    config = {}

    for section in parser.sections():
        config[section] = {}
        options = parser.options(section)
        for option in options:
            config[section][option] = parser.get(section, option)

    return config

if __name__ == '__main__':

    user_opts = read_options()
    config_file_path = user_opts.config_file
    config_data = read_config_file(config_file_path)

