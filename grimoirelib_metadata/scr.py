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

from grimoirelib_settings.settings import Settings

class SCR(DataSource):
    """ Class that adds and filters data in a Bicho-Gerrit-type database
    """

    # Meta table name
    METATABLE_NAME = Settings.SCR_METATABLE_NAME

    # Constants used to specify new columns to add to the metatable

    DATA_ORGANIZATIONS = "organizations" # Organizations info per changeset
    DATA_COUNTRIES = "countries"         # Countries info per changeset
    DATA_DOMAINS = "domains"             # Domains info per changeset
    DATA_BRANCHES = "branches"           # Branches used per changeset
    DATA_TIME2CLOSE = "time2close"       # Time to close per changeset
                                         # If this is merged, then this is time2merge
                                         # If this is abandoned, then this is time2abandon
    DATA_TIME_WAIT4REVIEWER = "timewaitingreviewer" # Total time waiting for reviewer action
    DATA_TIME_WAIT4SUBMITTER = "timewaitingsubmitter" # Total time waiting for submitter

    # Constants used to filter information from the metatable
    FILTER_BOTS = "bots"
    FILTER_ABANDONED = "abandoned"
    FILTER_OPEN = "open"
    FILTER_MERGED = "merged"
    FILTER_START_DATE = "startdate"
    FILTER_END_DATE = "enddate"


    def __init__(self, options):
        """ Init the SCR class

        :param options: config file options
        """

        # Initializing the dictionary with addition of new columns
        # and their correspondandt private methods
        self.new_columns = {}
        self.new_columns[SCR.DATA_ORGANIZATIONS] = self._add_column_organizations
        self.new_columns[SCR.DATA_COUNTRIES] = self._add_column_countries
        self.new_columns[SCR.DATA_DOMAINS] = self._add_column_domains
        self.new_columns[SCR.DATA_BRANCHES] = self._add_column_branches
        self.new_columns[SCR.DATA_TIME2CLOSE] = self._add_column_time2close
        self.new_columns[SCR.DATA_TIME_WAIT4REVIEWER] = self._add_column_time4reviewer
        self.new_columns[SCR.DATA_TIME_WAIT4SUBMITTER] = self._add_column_time4submitter

        # Initializing the dictionary with filters to be applied
        # and their methods
        self.filters = {}
        self.filters[SCR.FILTER_BOTS] = self._add_filter_bots
        self.filters[SCR.FILTER_ABANDONED] = self._add_filter_abandoned
        self.filters[SCR.FILTER_OPEN] = self._add_filter_open
        self.filters[SCR.FILTER_MERGED] = self._add_filter_merged
        self.filters[SCR.FILTER_START_DATE] = self._add_filter_startdate
        self.filters[SCR.FILTER_END_DATE] = self._add_filter_enddate

        # Initializing database options
        self.scr_db = options["databases"]["scr"]
        self.identities_db = options["databases"]["identities"]
        self.user_db = options["databases_access"]["user"]
        self.password_db = options["databases_access"]["password"]

        # By default, if the Bicho-Gerrit tool schema is used, the following fields
        # are used to build the basic metatable:
        # issues.issue, issues.status.author_date, scmlog.repository_id
        self.db, self.cursor = self._init_metatable()
        print "Init database correct"

    def _add_column_organizations(self):
        """ This private method adds a new column with organizations info.

        This takes into account the initial and final date of enrollment of a
        developer in a company.

        Information is found in the 'enrollments' table, created by SortingHat.
        """

        print "Adding column organizations"
        query = """ ALTER TABLE %s
                    ADD organizations INTEGER(11)
                """ % (SCR.METATABLE_NAME)
        self.cursor.execute(query)

        query = """UPDATE %s sm,
                          people_uidentities pui,
                          %s.enrollments enr
                   SET sm.organizations = enr.organization_id
                   WHERE sm.patchset_author = pui.people_id AND
                         pui.uuid = enr.uuid AND
                         sm.changeset_opened_on >= enr.start AND
                         sm.changeset_opened_on < enr.end
                """ % (SCR.METATABLE_NAME, self.identities_db)
        self.cursor.execute(query)

    def _add_column_countries(self):
        """ This private method adds a new column with countries info.

        Information is found in the 'profiles' table, created by SortingHat.
        """

        query = """ ALTER TABLE %s
                    ADD countries VARCHAR(2)
                """ % (SCR.METATABLE_NAME)
        self.cursor.execute(query)
        query = """UPDATE %s sm,
                          people_uidentities pui,
                          %s.profiles pro
                   SET sm.countries = pro.country_code
                   WHERE sm.patchset_author = pui.people_id AND
                         pui.uuid = pro.uuid
                """ % (SCR.METATABLE_NAME, self.identities_db)
        self.cursor.execute(query)

    def _add_column_domains(self):
        pass

    def _add_column_branches(self):
        pass

    def _add_column_time2close(self):
        pass

    def _add_column_time4reviewer(self):
        pass

    def _add_column_time4submitter(self):
        pass

    def add_annotation(self, metric):
        """ An new annotation adds a new column with the specified 'metric'

        :param metric: contains the name of the new column to be added
        """
        self.new_columns[metric]()

    def _add_filter_bots(self, values):
        pass

    def _add_filter_abandoned(self, values):
        pass

    def _add_filter_open(self, values):
        pass

    def _add_filter_merged(self, values):
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

        db, cursor = self._db_connection(self.user_db, self.password_db, self.scr_db)

        subquery_iterations = """ (SELECT ch.issue_id as issue_id,
                                         count(distinct(old_value)) as iterations
                                  FROM changes ch
                                  WHERE old_value <> ''
                                  GROUP BY ch.issue_id) it
                              """

        query = """ CREATE TABLE %s as
                            SELECT i.issue as gerrit_issue,
                                   i.status as current_status,
                                   i.submitted_by as patchset_author,
                                   ch.changed_on changeset_opened_on,
                                   i.tracker_id as gerrit_project,
                                   count(distinct(c.id)) as comments,
                                   it.iterations
                            FROM issues i,
                                 comments c,
                                 changes ch,
                                 %s
                            WHERE i.id = c.issue_id AND
                                  i.id = ch.issue_id AND
                                  ch.new_value = 'NEW' AND
                                  i.id = it.issue_id
                            GROUP BY i.issue
                """ % (SCR.METATABLE_NAME, subquery_iterations)
        cursor.execute(query)

        query = "ALTER TABLE %s ENGINE = MyISAM" % (SCR.METATABLE_NAME)
        cursor.execute(query)

        return db, cursor

