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

import MySQLdb

class DataSource(object):
    """ Abstract class used to build a Metrics Grimoire metadata database
    """

    def _db_connection(self, user, password, database,
                       host="127.0.0.1", port=3306, group=None):
        """ Database connection

        This method starts a connection with the provided database

        :param user: user name to access the database
        :param password: password used to access the database
        :param database: name of the database
        :param host: host where the database is located, by default: localhost
        :param port: port where the MySQL server is located
        :para group: group of the db connection
        """

        if group is None:
            db = MySQLdb.connect(user=user, passwd=password,
                                 db=database, host=host, port=port)
        else:
            db = MySQLdb.connect(read_default_group=group, db=database)

        cursor = db.cursor()
        cursor.execute("SET NAMES 'utf8'")

        return db, db.cursor()

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

    def _init_metatable(self):
        """ Create the basic metatable with initial information

        This table contains initial information from the core tables.
        """

        raise NotImplementedError

