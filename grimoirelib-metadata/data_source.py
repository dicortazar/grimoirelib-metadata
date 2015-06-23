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


class DataSource(object):
    """ Abstract class used to build a Metrics Grimoire metadata database
    """

    def add_annotation(self, metric):
        """ An new annotation adds a new column with the specified 'metric'

        :param metric: contains the name of the new column to be added
        """

        raise NotImplementedError

    def add_filter(self, filter_, values=None):
        """ Add a new filter to the already created metadata.

        This type of filters should be used as 'global' ones that will
        affect all of the metrics to be analyzed. An example of this type
        of filter is to remove 'merges' from a list of analysis.

        :param filter_: contains the type of filter to be applied
        :param values: contains the values to be applied to such filter_
        """

        raise NotImplementedError

