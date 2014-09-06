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

from abc import ABCMeta, abstractmethod

class DBUtility(object):
    __metaclass__ = ABCMeta
    
    def __init__(self):
        self.name = ''

    @abstractmethod
    def addOption(self, sparser):
        pass

    def getOption(self, args):
        pass

    @abstractmethod
    def createODBCConnection(self):
        pass
    
    @abstractmethod
    def closeODBCConnection(self):
        pass

    @abstractmethod
    def createDatabase(self, name):
        pass

    @abstractmethod
    def dropDatabase(self, name):
        pass
 
    @abstractmethod
    def useDatabase(self, name):
        pass

    @abstractmethod
    def createSchema(self, name):
        pass

    @abstractmethod
    def dropSchema(self, name):
        pass

    @abstractmethod
    def createTable(self):
        pass
  
    @abstractmethod
    def dropTable(self):
        pass

    @abstractmethod
    def createView(self):
        pass

    @abstractmethod
    def dropView(self):
        pass
    
    @abstractmethod
    def insertRow(self):
        pass

    @abstractmethod
    def run(self):
        pass

