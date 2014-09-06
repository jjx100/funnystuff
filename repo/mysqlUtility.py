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
import pyodbc 
import os, re, sys, glob, shutil, subprocess
from multiprocessing import Process, Pool, cpu_count
from datetime import datetime

#Define global variable to pass to versioning static method. 
#In order to avoid passing it via cmd parameters which could be shown by ps -ef. 
user = None
passwrod = None

def unwrapVersioningInstallSingleFile(args):
    return MysqlUtility.versioningInstallSingleFile(*args)

class MysqlUtility(DBUtility):
    special_ddl_files = ['configuration_tables.ddl',
                         'dimension_tables.ddl', 
                         'configuration_views.ddl',
                         'dimension_views.ddl',
                         'configuration_tables.insert',
                         'dimension_tables.insert']
    regular_ddl_pattern = ['*.proto.ddl']
    seapilot_home = os.getenv('SEAPILOT_HOME', '') 
    scripts_dir = os.getenv('SEAPILOT_HOME', '') + os.sep + 'mi' + os.sep + 'mysql' + os.sep + 'repository' + os.sep + 'scripts'
    fresh_log_base_name = 'fresh.log'
    versioning_log_base_name = 'versioning.log'
    def __init__(self):
        self.name = 'mysql'
        self.has_success = None
        self.has_failure = None

    def addOption(self, sparser):
        credentials = self.getCredentials().split()
        defaultUser = None
        defaultPassword = None
        if len(credentials) == 2:
            defaultUser, defaultPassword = credentials
        
        parser_mysql = sparser.add_parser('mysql', help='mysql help')
        group = parser_mysql.add_mutually_exclusive_group(required=True)
        group.add_argument('--initdb', nargs=1, metavar='DDL_PATH', help='Create tables and views in DDL_PATH.')
        group.add_argument('--cleandb', action='store_true', help='Drop database.')
        parser_mysql.add_argument('-d', '--database', required=True, help='Mysql database name')
        parser_mysql.add_argument('-u', '--user', nargs='?', const=defaultUser, default=defaultUser, help='Mysql user for login')
        parser_mysql.add_argument('-p', '--password', nargs='?', const=defaultPassword, default=defaultPassword, help='Mysql user password for login')

    def getOption(self, args):
        if args.initdb is not None:
            self.action = 'initdb'
            self.path = args.initdb[0]
            if not os.path.exists(self.path):
                print("DDL_PATH doesn't exist. Exit!")
                sys.exit(1)
        elif args.cleandb is True:
            self.action = 'cleandb'
        self.database = args.database
        self.user = args.user
        self.password = args.password

        global user, password
        user = self.user
        password = self.password

    def getCredentials(self):
        #Get the stdout from the script. Ignore the stderr output.
        return subprocess.Popen(['sp_set_odbc.sh'], stdout=subprocess.PIPE).communicate()[0]

    def createODBCConnection(self):
        try:
            self.cnxn = pyodbc.connect('DSN=sp2mysql;Server=localhost;Database=information_schema;UID={0};PWD={1};Option=3;CHARSET=UTF8;'.format(self.user, self.password))
            self.cursor = self.cnxn.cursor()
        except pyodbc.Error as e:
            print('Failed')
            print('Error:' ,e)
            sys.exit(1)

    def closeODBCConnection(self):
        self.cnxn.close()

    def createDatabase(self, name = ''):
        sql = 'create database ' + name
        self.executeHelper(sql)

    def dropDatabase(self, name):
        sql = 'drop database ' + name
        self.executeHelper(sql)

    def useDatabase(self, name):
        sql = 'use ' + name
        self.executeHelper(sql)

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
        self.createODBCConnection()
        if self.action == 'initdb':
            if self.isClean():
                self.freshInstall()
            else:
                self.versioningInstall()
        elif self.action == 'cleandb':
            self.dropDatabase(self.database)
        self.closeODBCConnection()

    def isClean(self):
        self.cursor.execute('show databases;')
        rows = self.cursor.fetchall()
        for row in rows:
            if self.database == 'information_schema':
                raise Exception("Can't do operation in information_schema. Choose another database.")
            elif self.database == 'mysql':
                raise Exception("Can't do operation in mysql. Choose another database.")
            elif row.Database == self.database:
                return False
        else:
            return True

    def freshInstall(self):
        freshlogfile = MysqlUtility.scripts_dir + os.sep + MysqlUtility.fresh_log_base_name
        freshlogfd = open(freshlogfile, 'w')
        
        MysqlUtility.printHelper('title', 'Repository Utility', fileout=freshlogfd)
        MysqlUtility.printHelper('title', 'Fresh install starting', fileout=freshlogfd)
        MysqlUtility.printHelper('segment', 'Create database ' + self.database, fileout=freshlogfd)
        self.createDatabase(self.database)
        self.useDatabase(self.database)
        
        #Execute the ddl in special files first.
        for file in MysqlUtility.special_ddl_files:
            self.freshInstallSingleFile(file, freshlogfd)
        
        for pattern in MysqlUtility.regular_ddl_pattern:
            files = glob.glob(self.path + os.sep + pattern)
            for file in sorted(files):
                self.freshInstallSingleFile(os.path.basename(file), freshlogfd)
       
        if self.has_success == True and self.has_failure is None: 
            MysqlUtility.printHelper('title', 'Fresh install successfully completed', fileout=freshlogfd)
        elif self.has_success == True and self.has_failure == True:
            MysqlUtility.printHelper('title', 'Fresh install partially completed, see errors above', fileout=freshlogfd)
        elif self.has_success is None and self.has_failure == True:
            MysqlUtility.printHelper('title', 'Fresh install failed', fileout=freshlogfd)
        freshlogfd.close()

    def freshInstallSingleFile(self, file, logfile):
        MysqlUtility.printHelper('segment', 'Execute sql in ' + file, fileout=logfile)
        file = self.path + os.sep + file
        if os.path.exists(file):
            with open(file, 'r') as readfile:
                results = re.findall('^[ \t]*[a-zA-Z]+?.+?;', readfile.read(), re.IGNORECASE | 
                                                                               re.DOTALL | 
                                                                               re.MULTILINE)
                for i, v in enumerate(results):
                   self.executeHelper(v, fileout=logfile)
                   #Add extra empty line
                   MysqlUtility.printHelper('free', '', fileout=logfile) 

    def versioningInstall(self):
        MysqlUtility.printHelper('title', 'Repository Utility')
        MysqlUtility.printHelper('title', 'Versioning install starting')

        self.useDatabase(self.database)
        tempdb = 'tempdb_{0}'.format(datetime.utcnow().strftime('%Y_%m_%d_%H_%M_%S'))
        self.createDatabase(tempdb)

        pool1 = Pool(processes=1)
        pool2 = Pool(processes=cpu_count())

        try:
            special_ddl_files_with_path = [ self.path + os.sep + x for x in MysqlUtility.special_ddl_files ]  
            results1 = pool1.map(unwrapVersioningInstallSingleFile, zip(special_ddl_files_with_path,
                                                                       [self.database]*len(MysqlUtility.special_ddl_files),
                                                                       [tempdb]*len(MysqlUtility.special_ddl_files)))
            pool1.close()
            pool1.join()

            for pattern in MysqlUtility.regular_ddl_pattern:
                files = sorted(glob.glob(self.path + os.sep + pattern))
                results2 = pool2.map(unwrapVersioningInstallSingleFile, zip(files, 
                                                                            [self.database]*len(files), 
                                                                            [tempdb]*len(files)))
            pool2.close()
            pool2.join()
        except KeyboardInterrupt:
            pool1.terminate()
            pool2.terminate()
            pool1.join()
            pool2.join()
            sys.exit(1)

        self.dropDatabase(tempdb)

        #Merge standalone log files into one file.
        finallogname = MysqlUtility.scripts_dir + os.sep + 'versioning_details.log'
        with open(finallogname, 'w') as finallog:
            for log in sorted(glob.glob(MysqlUtility.scripts_dir + os.sep + '*.tlog')):
                shutil.copyfileobj(open(log, 'r'), finallog)
                os.remove(log)
        MysqlUtility.printHelper('free', 'logfile ' + finallogname + ' generated.')

        results = results1 + results2
        for i in results:
            if i != 0:
                MysqlUtility.printHelper('title', 'Versioning install partially completed, see errors in versioning details log')
                break
        else:
            MysqlUtility.printHelper('title', 'Versioning install successfully completed')

    def versioningInstallSingleFile(ddlfile, targetdb, tempdb):
        try:
            retCode = 0
            MysqlUtility.printHelper('free', 'Processing ' + ddlfile + ' in background...')
            cnxn = pyodbc.connect('DSN=sp2mysql;Server=localhost;'
                                  'Database=information_schema;'
                                  'UID={0};PWD={1};'
                                  'Option=3;CHARSET=UTF8;'.format(user, password))
            cursor = cnxn.cursor()
            logbasename = os.path.basename(ddlfile) + '.tlog'
            logfile = MysqlUtility.scripts_dir + os.sep + logbasename
            logfd = open(logfile, 'w')

            MysqlUtility.printHelper('title', 'processing file {0} begin'.format(os.path.basename(ddlfile)), False, logfd)
        
            #Get the list of installed tables in target database.
            cursor.execute('use ' + targetdb)
            cursor.execute("select table_name from information_schema.tables where table_type = 'BASE TABLE' and table_schema = '{0}'".format(targetdb))
            rows = cursor.fetchall()
            tablesInTargetdb = [ x[0] for x in rows ]
 
            #Prepare the regular expression for later use.
            tablere = re.compile('^[ \t]*create[ \t]+table[ \t]+(\w+).+?;', re.IGNORECASE | re.DOTALL | re.MULTILINE)
            viewre = re.compile('^[ \t]*create[ \t]+view[ \t]+(\w+).+?;', re.IGNORECASE | re.DOTALL | re.MULTILINE)

            with open(ddlfile, 'r') as readfile:
                results = re.findall('^[ \t]*[a-zA-Z]+?.+?;', readfile.read(), re.IGNORECASE | re.DOTALL | re.MULTILINE)
                for i, v in enumerate(results):
                    try:
                        tablereobj = tablere.match(v)                    
                        viewreobj = viewre.match(v)

                        if tablereobj is not None:
                            table = tablereobj.group(1)
                            if table in tablesInTargetdb:
                                tempTableMetaData = []
                                tempTablePrimaryKeys = []
                                #Create temp table in temp schema
                                cursor.execute('use ' + tempdb)
                                cursor.execute(v)
                                for eachRow in cursor.columns(table):
                                    tempTableMetaData.append((eachRow.column_name, eachRow.type_name, 
                                                              eachRow.column_size, eachRow.is_nullable))
                                for eachRow in cursor.primaryKeys(table):
                                    tempTablePrimaryKeys.append(eachRow.column_name)
                            
                                targetTableMetaData = []
                                targetTablePrimaryKeys = []
                                cursor.execute('use ' + targetdb)
                                for eachRow in cursor.columns(table):
                                    targetTableMetaData.append((eachRow.column_name, eachRow.type_name, 
                                                                eachRow.column_size, eachRow.is_nullable))
                                for eachRow in cursor.primaryKeys(table):
                                    targetTablePrimaryKeys.append(eachRow.column_name)

                                tableIsSame = True
                                if (len(tempTableMetaData) != len(targetTableMetaData) or 
                                    len(tempTablePrimaryKeys) != len(targetTablePrimaryKeys)):
                                    tableIsSame = False
                                else:
                                    for (x, y) in zip(tempTableMetaData, targetTableMetaData):
                                        if x != y:
                                            tableIsSame = False

                                    for (x, y) in zip(tempTablePrimaryKeys, targetTablePrimaryKeys):
                                        if x != y:
                                            tableIsSame = False
                            
                                if not tableIsSame:
                                    MysqlUtility.printHelper('segment', 'Table ' + table + ' is different.' , False, fileout=logfd)
                                    tableRename = table + datetime.utcnow().strftime('%Y_%m_%d_%H_%M_%S')
                                    MysqlUtility.printHelper('segment', 'Rename old table to ' + tableRename, False, fileout=logfd)
                                    cursor.execute('rename table ' + table + ' to ' + tableRename)
                                    MysqlUtility.printHelper('segment', 'Create new table ' + table, False, fileout=logfd)
                                    MysqlUtility.printHelper('free', v, False, fileout=logfd) 
                                    cursor.execute(v)
                                else:
                                    MysqlUtility.printHelper('segment', 'Table ' + table + ' is same.', False, fileout=logfd)

                            else:
                                MysqlUtility.printHelper('segment', 'Table ' + table + " doesn't exist. Create it now...", False, fileout=logfd)
                                cursor.execute('use ' + targetdb)
                                MysqlUtility.printHelper('free', v, False, fileout=logfd)
                                cursor.execute(v)
                            
                        elif viewreobj is not None:
                            view = viewreobj.group(1)
                            MysqlUtility.printHelper('segment', 'Drop and recreate view ' + view, False, fileout=logfd)
                            cursor.execute('use ' + targetdb)
                            MysqlUtility.printHelper('free', 'drop view ' + view, False, fileout=logfd)
                            #Ignore the drop view error. The status should depends on create view.
                            try:
                                cursor.execute('drop view ' + view)
                            except pyodbc.Error:
                                pass
                            MysqlUtility.printHelper('free', v, False, fileout=logfd)
                            cursor.execute(v)
                        else:  
                            MysqlUtility.printHelper('segment', 'Execute sql: ', False, fileout=logfd)
                            cursor.execute('use ' + targetdb) 
                            MysqlUtility.printHelper('free', v, False, fileout=logfd)
                            cursor.execute(v)
                    except pyodbc.OperationalError:
                        raise
                    except pyodbc.InternalError:
                        raise
                    except pyodbc.NotSupportedError:
                        raise
                    except pyodbc.DatabaseError as e:
                        MysqlUtility.printHelper('free', 'Failed', False, fileout=logfd)
                        MysqlUtility.printHelper('free', 'Error:' + repr(e), False, fileout=logfd)
                        retCode = 1
                    except pyodbc.Error as e:
                        MysqlUtility.printHelper('free', 'Failed', False, fileout=logfd)
                        MysqlUtility.printHelper('free', 'Error:' + repr(e), False, fileout=logfd)
                        retCode = 1
                    else:
                        MysqlUtility.printHelper('free', 'Succeeded', False, fileout=logfd)
                MysqlUtility.printHelper('title', 'processing file {0} end'.format(os.path.basename(ddlfile)), False, fileout=logfd)
            logfd.close()
            cnxn.close()
            return retCode
        except KeyboardInterrupt:
            return 1
        
    def displaymatch(match):
        if match is None:
            return None
        return '<Match: {0}, groups={1}>'.format(match.group(), match.groups())

    def printHelper(pos, str, stdout=True, fileout=None):
        if stdout:
            if pos == 'title':
                print('-'*20, '{0:-<60}'.format(str), sep='')
            elif pos == 'segment':
                print('~'*4, str, sep='')
            elif pos == 'free':
                print(str)
        
        if fileout:
            if pos == 'title':
                print('-'*20, '{0:-<60}'.format(str), sep='', file=fileout)
            elif pos == 'segment':
                print('~'*4, str, sep='', file=fileout)
            elif pos == 'free':
                print(str, file=fileout)
       
    
    def executeHelper(self, sql, stdout=True, fileout=None):
        if stdout:
            print(sql)
        if fileout:
            print(sql, file=fileout)
        try:
            self.cursor.execute(sql)
        except pyodbc.OperationalError:
            raise
        except pyodbc.InternalError:
            raise
        except pyodbc.NotSupportedError:
            raise
        except pyodbc.DatabaseError as e:
            if stdout:
                print('Failed')
                print('Error:' ,e)
            if fileout:
                print('Failed', file=fileout)
                print('Error:' ,e, file=fileout)
            self.has_failure = True
        except pyodbc.Error as e:
            if stdout:
                print('Failed')
                print('Error:' ,e)
            if fileout:
                print('Failed', file=fileout)
                print('Error:' ,e, file=fileout)
            self.has_failure = True
        else:
            if stdout:
                print('Succeeded')
            if fileout:
                print('Succeeded', file=fileout)
            self.has_success = True


    displaymatch = staticmethod(displaymatch)
    printHelper = staticmethod(printHelper)
    versioningInstallSingleFile = staticmethod(versioningInstallSingleFile)
