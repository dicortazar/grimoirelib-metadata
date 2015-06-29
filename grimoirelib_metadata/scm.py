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

from grimoirelib_metadata.data_source import DataSource

class SCM(DataSource):
    """ Class that adds and filters data in a CVSAnalY-type database
    """

    # Meta table name
    METATABLE_NAME = "scm_metadata"

    # Constants used to specify new columns to add to the metatable
    DATA_ORGANIZATIONS = "organizations"
    DATA_COUNTRIES = "countries"
    DATA_DOMAINS = "domains"
    DATA_BRANCHES = "branches"
    DATA_LINES = "lines"
    DATA_BOTS = "bots"

    # Constants used to filter information from the metatable
    FILTER_MERGES = "merges"
    FILTER_START_DATE = "startdate"
    FILTER_END_DATE = "enddate"


    def __init__(self, options):
        """ Init the SCM class

        :param options: config file options
        """

        # Initializing the dictionary with addition of new columns
        # and their correspondandt private methods
        self.new_columns = {}
        self.new_columns[SCM.DATA_ORGANIZATIONS] = self._add_column_organizations
        self.new_columns[SCM.DATA_COUNTRIES] = self._add_column_countries
        self.new_columns[SCM.DATA_DOMAINS] = self._add_column_domains
        self.new_columns[SCM.DATA_BRANCHES] = self._add_column_branches
        self.new_columns[SCM.DATA_LINES] = self._add_column_lines

        # Initializing the dictionary with filters to be applied
        # and their methods
        self.filters = {}
        self.filters[SCM.FILTER_MERGES] = self._add_filter_merges
        self.filters[SCM.FILTER_START_DATE] = self._add_filter_startdate
        self.filters[SCM.FILTER_END_DATE] = self._add_filter_enddate

        # Initializing database options
        self.scm_db = options["databases"]["scm"]
        self.identities_db = options["databases"]["identities"]
        self.user_db = options["databases_access"]["user"]
        self.password_db = options["databases_access"]["password"]

        # By default, if the CVSAnalY tool schema is used, the following fields
        # are used to build the basic metatable:
        # scmlog.id, scmlog.author_id, scmlog.author_date, scmlog.repository_id
        self.db, self.cursor = self._init_metatable()
        print "Init database correct"

    def _add_column_organizations(self):
        """ This private method adds a new column with organizations info.

        This takes into account the initial and final date of enrollment of a
        developer in a company.

        Information is found in the 'enrollments' table, created by SortingHat.
        """

        query = """ ALTER TABLE %s
                    ADD organizations INTEGER(11)
                """ % (SCM.METATABLE_NAME)
        self.cursor.execute(query)

        query = """UPDATE %s sm,
                          people_uidentities pui,
                          %s.enrollments enr
                   SET sm.organizations = enr.organization_id
                   WHERE sm.author = pui.people_id AND
                         pui.uuid = enr.uuid AND
                         sm.date >= enr.start and sm.date < enr.end
                """ % (SCM.METATABLE_NAME, self.identities_db)
        self.cursor.execute(query)

    def _add_column_countries(self):
        """ This private method adds a new column with countries info.

        Information is found in the 'profiles' table, created by SortingHat.
        """

        query = """ ALTER TABLE %s
                    ADD countries VARCHAR(2)
                """ % (SCM.METATABLE_NAME)
        self.cursor.execute(query)
        query = """UPDATE %s sm,
                          people_uidentities pui,
                          %s.profiles pro
                   SET sm.countries = pro.country_code
                   WHERE sm.author = pui.people_id AND
                         pui.uuid = pro.uuid
                """ % (SCM.METATABLE_NAME, self.identities_db)
        self.cursor.execute(query)

    def _add_column_domains(self):
        pass

    def _add_column_branches(self):
        pass

    def _add_column_lines(self):
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

    def _init_metatable(self):

        db, cursor = self._db_connection(self.user_db, self.password_db, self.scm_db)
        query = """ CREATE TABLE %s as
                            SELECT id as commit,
                                   author_id as author,
                                   author_date as date,
                                   repository_id as repository
                            FROM scmlog
                """ % (SCM.METATABLE_NAME)
        cursor.execute(query)

        query = "ALTER TABLE %s ENGINE = MYISAM" % (SCM.METATABLE_NAME)
        cursor.execute(query)

        return db, cursor

