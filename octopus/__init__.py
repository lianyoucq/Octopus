# -*- coding:utf-8 -*-
from datetime import datetime

from flask import Flask, make_response, jsonify, g
from flask_restful import Api

from config import Config
from octopus.common.logger import mainLogger
from octopus.common.path_utils import get_work_dir
from octopus.database import db
from octopus.database.metadata import Domain, INFA_ENV, Node
from octopus.views.api.infa.infacmd.dis import infacmd_dis_bp, ListApplications, ListApplicationObjects, \
    StopBlazeService, \
    BackupApplication, StopApplication, StartApplication
from octopus.views.api.infa.infacmd.isp import infacmd_isp_bp, Ping, ResetPassword, PurgeLog, EnableServiceProcess, \
    DisableServiceProcess, EnableService, DisableService, ListNodeResources, ListNodes, ListServiceLevels, ListServices, \
    ListServiceNodes, ListServicePrivileges, GetServiceStatus, ListLicenses, ShowLicense, ListAllUsers, ListConnections, \
    ListConnectionOptions, ListUserPermissions, ListUserPrivileges, ListGroupsForUser
from octopus.views.api.infa.infacmd.mrs import infacmd_mrs_bp, BackupContents
from octopus.views.api.infa.infacmd.ms import infacmd_ms_bp, ListMappings, RunMapping, GetMappingStatus, GetRequestLog, \
    ListMappingParams
from octopus.views.api.infa.infacmd.oie import DeployApplication, infacmd_oie_bp
from octopus.views.api.infa.infacmd.wfs import StartWorkflow, ListWorkflows, ListTasks, ListActiveWorkflowInstances, \
    ListWorkflowParams, infacmd_wfs_bp
from octopus.views.api.infa.infasetup import Backup_domain, infasetup_bp
from octopus.views.api.infa.utils import utils_bp, Pmpassword
from octopus.views.api.mgt.innerdb import mgt_idb_bp, IDB, InfaEnvs

## markdown
# from flaskext.markdown import Markdown

__author__ = "Arthur Li"
__email__ = "845201629@qq.com"
__version__ = "1.0.0"

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
app.config.update(SQLALCHEMY_BINDS={
    'octopus_db': Config.SQLALCHEMY_DATABASE_URI,
    'octopus_inner': "sqlite:///{0}/config.db".format(get_work_dir())
})

# json 正确显示中文，而不是unicode
app.config.update(RESTFUL_JSON=dict(ensure_ascii=False))


# Markdown(app)
# @app.route("/")
# def index():
#     contents = ""
#     with open("README.md", 'r') as freadme:
#         for i in  freadme.readlines():
#             contents += str(i)
#     template = '{{mystr|markdown}}'
#     print(type(contents))
#     return render_template_string(template, mystr = contents)

# app handler
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(Exception)
def internal_error(exception):
    print("######### {0}".format(exception))
    # excepMsg = [str(x) for x in exception.args]
    excepMsg = "Error: " + str(exception.args)[1:-1]
    return excepMsg, 500


@app.before_first_request
def before_first_request():
    print("########### Init the inner db")
    try:
        db.create_all(bind="octopus_inner")
    except Exception as e:
        mainLogger.exception(str(e))
        raise Exception(e)


@app.before_request
def my_before_request():
    print("################# locals = {0}".format(locals()))
    g.startTime = datetime.now()


@app.after_request
def my_after_request(param):
    endTime = datetime.now()
    delta_time = endTime - g.startTime
    total_seconds = delta_time.total_seconds()
    mainLogger.debug(
        "######  my_after_request is invoked, and total_seconds is {0}, and param is {1}".format(total_seconds,
                                                                                                 param))
    return param


# 注入 infasetup 视图
infasetup_api = Api(infasetup_bp)
infasetup_api.add_resource(Backup_domain, '/backupdomain')
app.register_blueprint(infasetup_bp, url_prefix="/api/infa/infasetup")

# 注入utils 视图
utils_api = Api(utils_bp)
utils_api.add_resource(Pmpassword, "/pmpasswd")
app.register_blueprint(utils_bp, url_prefix="/api/infa/utils")

# 注入infacmd isp视图
infacmd_isp_api = Api(infacmd_isp_bp)
infacmd_isp_api.add_resource(Ping, "/ping")
infacmd_isp_api.add_resource(ResetPassword, "/resetpassword")
infacmd_isp_api.add_resource(PurgeLog, "/purgelog")
infacmd_isp_api.add_resource(EnableServiceProcess, "/enableserviceprocess")
infacmd_isp_api.add_resource(DisableServiceProcess, "/disableserviceprocess")
infacmd_isp_api.add_resource(EnableService, "/enableservice")
infacmd_isp_api.add_resource(DisableService, "/disableservice")
infacmd_isp_api.add_resource(ListNodes, '/listnodes')
infacmd_isp_api.add_resource(ListNodeResources, '/listnoderesources')
infacmd_isp_api.add_resource(ListServiceLevels, '/listservicelevels')
infacmd_isp_api.add_resource(ListServices, '/listservices')
infacmd_isp_api.add_resource(ListServiceNodes, '/listservicenodes')
infacmd_isp_api.add_resource(ListServicePrivileges, '/listserviceprivileges')
infacmd_isp_api.add_resource(GetServiceStatus, '/getservicestatus')
infacmd_isp_api.add_resource(ListLicenses, '/listlicenses')
infacmd_isp_api.add_resource(ShowLicense, '/showlicense')
infacmd_isp_api.add_resource(ListAllUsers, '/listallusers')
infacmd_isp_api.add_resource(ListConnections, '/listconnections')
infacmd_isp_api.add_resource(ListConnectionOptions, '/listconnectionoptions')
infacmd_isp_api.add_resource(ListUserPermissions, '/listuserpermissions')
infacmd_isp_api.add_resource(ListUserPrivileges, '/listuserprivileges')
infacmd_isp_api.add_resource(ListGroupsForUser, '/listgroupsforuser')
app.register_blueprint(infacmd_isp_bp, url_prefix="/api/infa/infacmd/isp")

# 注入infacmd - dis 视图
infacmd_dis_api = Api(infacmd_dis_bp)
infacmd_dis_api.add_resource(ListApplications, '/listapplications')
infacmd_dis_api.add_resource(ListApplicationObjects, '/listapplicationobjects')
infacmd_dis_api.add_resource(StopBlazeService, '/stopblazeservice')
infacmd_dis_api.add_resource(BackupApplication, '/backupapplication')
infacmd_dis_api.add_resource(StopApplication, '/stopapplication')
infacmd_dis_api.add_resource(StartApplication, '/startapplication')
app.register_blueprint(infacmd_dis_bp, url_prefix="/api/infa/infacmd/dis")

# 注入infacmd - mrs视图
infacmd_mrs_api = Api(infacmd_mrs_bp)
infacmd_mrs_api.add_resource(BackupContents, "/backupcontents")
app.register_blueprint(infacmd_mrs_bp, url_prefix="/api/infacmd/mrs")

# 注入infacmd - ms视图
infacmd_ms_api = Api(infacmd_ms_bp)
infacmd_ms_api.add_resource(ListMappings, "/listmappings")
infacmd_ms_api.add_resource(RunMapping, "/runmapping")
infacmd_ms_api.add_resource(GetMappingStatus, "/getmappingstatus")
infacmd_ms_api.add_resource(GetRequestLog, "/getrequestlog")
infacmd_ms_api.add_resource(ListMappingParams, "/listmappingparams")
app.register_blueprint(infacmd_ms_bp, url_prefix="/api/infa/infacmd/ms")

# 注入infacmd - oie视图
infacmd_oie_api = Api(infacmd_oie_bp)
infacmd_oie_api.add_resource(DeployApplication, '/deployapplication')
app.register_blueprint(infacmd_oie_bp, url_prefix="/api/infa/infacmd/oie")

# 注入infacmd - wfs视图
infacmd_wfs_api = Api(infacmd_wfs_bp)
infacmd_wfs_api.add_resource(StartWorkflow, '/startworkflow')
infacmd_wfs_api.add_resource(ListWorkflows, '/listworkflows')
infacmd_wfs_api.add_resource(ListTasks, '/listtasks')
infacmd_wfs_api.add_resource(ListActiveWorkflowInstances, '/listactiveworkflowinstances')
infacmd_wfs_api.add_resource(ListWorkflowParams, '/listworkflowparams')
app.register_blueprint(infacmd_wfs_bp, url_prefix="/api/infa/infacmd/wfs")

# Common APIs
# Inner DB
mgt_idb_api = Api(mgt_idb_bp)
# it's no need to invoke this function
# mgt_idb_api.add_resource(InitIDB, "/init")
# mgt_idb_api.add_resource(LoadIDB, "/load")
# mgt_idb_api.add_resource(DropIDB, "/drop")
mgt_idb_api.add_resource(IDB, "/idb")


# INFA_ENV
# mgt_idb_api.add_resource(UpsertInfaEnvs, "/env/upsert")
mgt_idb_api.add_resource(InfaEnvs, "/env", endpoint="env")
mgt_idb_api.add_resource(InfaEnvs, "/env/<envs>")


app.register_blueprint(mgt_idb_bp, url_prefix="/api/mgt")


