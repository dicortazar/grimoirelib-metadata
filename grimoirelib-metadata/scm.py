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


class SCM(object):
    """ Class that add and filter data in a CVSAnalY-type database
    """

    # Constants used to specify new columns to add to the metatable
    DATA_COMMITS = "commits"
    DATA_AUTHORS = "authors"
    DATA_AUTHORS_DATE = "authors_date"
    DATA_ORGANIZATIONS = "organizations"
    DATA_REPOSITORIES = "repositories"
    DATA_BRANCHES = "branches"

    # Constants used to filter information from the metatable
    FILTER_MERGES = "merges"
    FILTER_START_DATE = "startdate"
    FILTER_END_DATE = "enddate"


    def __init__(self):
        self.new_columns = {}
        self.new_columns[DATA_COMMITS] = self._add_column_commits
        self.new_columns[DATA_AUTHORS] = self._add_column_authors
        self.new_columns[DATA_AUTHORS_DATE] = self._add_column_authors_date
        self.new_columns[DATA_ORGANIZATIONS] = self._add_column_organizations
        self.new_columns[DATA_REPOSITORIES] = self._add_column_repositories
        self.new_columns[DATA_BRANCHES] = self._add_column_branches

        self.filters = {}
        self.filters[FILTER_MERGES] = self._add_filter_merges
        self.filters[FILTER_START_DATE] = self._add_filter_startdate
        self.filters[FILTER_END_DATE] = self._add_filter_enddate

    def _add_column_commits(self):
        pass

    def _add_column_authors(self):
        pass

    def _add_column_authors_date(self):
        pass

    def _add_column_organizations(self):
        pass

    def _add_column_repositories(self):
        pass

    def _add_column_branches(self):
        pass

    def add_annotation(self, metric):
        """ An new annotation adds a new column with the specified 'metric'

        :param metric: contains the name of the new column to be added
        """

        self.new_columns[metric]()

    def _add_filter_merges(self, values):
        pass

    def _add_filter_startdate(self, startdate):
        pass

    def _add_filter_enddate(self, enddate):
        pass


    def add_filter(self, filter_, values = None):
        """ Add a new filter to the already created metadata.

        This type of filters should be used as 'global' ones that will
        affect all of the metrics to be analyzed. An example of this type
        of filter is to remove 'merges' from a list of analysis.

        :param filter_: contains the type of filter to be applied
        :param values: contains the values to be applied to such filter_
        """

        self.filters[filter_](values)

