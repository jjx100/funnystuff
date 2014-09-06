#!/usr/bin/python
# @@@ START COPYRIGHT @@@
#
# (C) Copyright 2013-2014 Hewlett-Packard Development Company, L.P.
#
# @@@ END COPYRIGHT @@@
from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
#from __future__ import unicode_literals

from .dbUtility import DBUtility

class VerticaUtility(DBUtility):
    def __init__(self):
        self.name = 'vertica'
    
    def addOption(self, sparser):
        parser_vertica = sparser.add_parser('vertica', help='vertica help')
        parser_vertica.add_argument('-d', '--database', required=True, help='Vertica database name')
        parser_vertica.add_argument('-s', '--schema', required=True, help='Vertica schema name')
        parser_vertica.add_argument('-u', '--user', nargs='?', const='root', default='root', help='Vertica user for login')
        parser_vertica.add_argument('-p', '--password', nargs='?', const='seapilot', default='seapilot', help='User password for login')

    def getOption(self, args):
        pass

    def createODBCConnection(self):
        pass

    def closeODBCConnection(self):
        pass

    def createDatabase(self, name):
        pass

    def dropDatabase(self, name):
        pass

    def useDatabase(self, name):
        pass

    def createSchema(self, name):
        pass

    def dropSchema(self, name):
        pass

    def createTable(self):
        pass

    def dropTable(self):
        pass

    def createView(self):
        pass

    def dropView(self):
        pass

    def insertRow(self):
        pass

    def run(self):
        pass

