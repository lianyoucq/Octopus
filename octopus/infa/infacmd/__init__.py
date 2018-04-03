# -*- coding:utf-8 -*-
from collections import namedtuple

########################################################################################################################
#### data integration service
########################################################################################################################
from octopus.infa.infacmd.dis import (startApplication,
                                      listApplicationObjects, listApplications, stopBlazeService, backupApplication,
                                      startApplication, stopApplication
                                      )

########################################################################################################################
#### data integration service  - workflow
########################################################################################################################
from octopus.infa.infacmd.wfs import (startWorkflow, listWorkflows, listTasks, listActiveWorkflowInstances,
                                      listWorkflowParams)

########################################################################################################################
#### data integration service - mapping
########################################################################################################################
from octopus.infa.infacmd.ms import (listMappings, listMappingParams,
                                     runMapping,
                                     getMappingStatus, getRequestLog)

########################################################################################################################
#### informatica service platform
########################################################################################################################
from octopus.infa.infacmd.isp import (listServices, listServiceNodes, listServiceLevels, listServicePrivileges,
                                      getServiceStatus, listAllUsers, listConnections, listConnectionOptions,
                                      listLicenses, showLicense, listNodeResources, listNodes, listUserPermissions,
                                      listUserPrivileges, listGroupsForUser, purgeLog, resetPassword,
                                      enableServiceProcess, enableService, disableService, ping, )

########################################################################################################################
#### Model Repository Service
########################################################################################################################
from octopus.infa.infacmd.mrs import (backupContents)

########################################################################################################################
#### Service Type
########################################################################################################################
___servicetype_name__ = ['Analyst_Service',
                         'SAP_BW_Service',
                         'Content_Management_Service',
                         'Data_Integration_Service',
                         'Email_Service',
                         'Informatica_Cluster_Service',
                         'PowerCenter_Integration_Service',
                         'Live_Data_Map',
                         'Metadata_Manager_Service',
                         'Model_Repository_Service',
                         'Resource_Manager_Service',
                         'PowerCenter_Repository_Service',
                         'Scheduler_Service',
                         'Search_Service',
                         'Test_Data_Manager_Service',
                         'Test_Data_Warehouse_Service',
                         'Web_Service_Hub',
                         'Administrator_Console']
___servicetype_value__ = ['AS',
                          'BW',
                          'CMS',
                          'DIS',
                          'ES',
                          'IHS',
                          'IS',
                          'LDM',
                          'MM',
                          'MRS',
                          'RMS',
                          'RS',
                          'SCH',
                          'SEARCH',
                          'TDM',
                          'TDW',
                          'WS',
                          '_adminconsole']
__servicetype_namedtuple__ = namedtuple("serviceTypes", ___servicetype_name__)
servicetype_namedtuple = __servicetype_namedtuple__(*tuple(___servicetype_value__))

########################################################################################################################
#### Connection Type
########################################################################################################################
__connectiontype_name__ = [
    'VSAM',
    'SAP_Deprecated',
    'HTTP',
    'DB2I',
    'SQLSERVER',
    'IMS',
    'ORACLE',
    'WEBSERVICES',
    'ADABAS',
    'ODBC',
    'DB2',
    'DB2Z',
    'SEQ',
    'GreenplumPT',
    'TWITTER',
    'LINKEDIN',
    'HBASE',
    'LDAP',
    'MAPRSTREAMS',
    'AZUREDW',
    'ADLSV2',
    'AZUREBLOB',
    'TWITTERSTREAMING',
    'MSDYNAMICS',
    'SAPAPPLICATIONS',
    'TeradataPT',
    'JDBC',
    'AMAZONS3',
    'SALESFORCE',
    'ODATA',
    'TABLEAU',
    'DATASIFT',
    'HIVE',
    'AMAZONREDSHIFT',
    'SFDC',
    'FACEBOOK',
    'WEBCONTENT_KAPOWKATALYST',
    'HADOOP',
    'KAFKA',
    'HadoopFileSystem',
    'NETEZZA',
    'AMAZONKINESIS',
    'JDEE1',
    'JMS'
]
__connectiontype_value__ = [
    'VSAM',
    'SAP (Deprecated)',
    'HTTP',
    'DB2I',
    'SQLSERVER',
    'IMS',
    'ORACLE',
    'WEB SERVICES',
    'ADABAS',
    'ODBC',
    'DB2',
    'DB2Z',
    'SEQ',
    'GreenplumPT',
    'TWITTER',
    'LINKEDIN',
    'HBASE',
    'LDAP',
    'MAPRSTREAMS',
    'AZUREDW',
    'ADLSV2',
    'AZUREBLOB',
    'TWITTERSTREAMING',
    'MSDYNAMICS',
    'SAPAPPLICATIONS',
    'TeradataPT',
    'JDBC',
    'AMAZONS3',
    'SALESFORCE',
    'ODATA',
    'TABLEAU',
    'DATASIFT',
    'HIVE',
    'AMAZONREDSHIFT',
    'SFDC',
    'FACEBOOK',
    'WEBCONTENT - KAPOWKATALYST',
    'HADOOP',
    'KAFKA',
    'HadoopFileSystem',
    'NETEZZA',
    'AMAZONKINESIS',
    'JDEE1',
    'JMS',
]
__connectiontype_namedtuple__ = namedtuple("connectionTypes", __connectiontype_name__)
connectiontype_namedtupe = __connectiontype_namedtuple__(*tuple(__connectiontype_value__))
