# -*- coding:utf-8 -*-
import json
import os

from flask import Blueprint, make_response, g
from flask_restful import reqparse, Resource

from octopus.common import is_none
from octopus.common.logger import mainLogger
from octopus.database.metadata import get_current_node_infa_envs
from octopus.exceptions import MissingRequiredParametersException
from octopus.infa.infacmd.dis import listApplications, listApplicationObjects, stopBlazeService, backupApplication, \
    stopApplication, startApplication
from config import Config
from octopus.views.api import infaCliResponse_pb2

infacmd_dis_bp = Blueprint("dis", __name__)


class ListApplications(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("servicename", type=str, help="Required")
        self.parser.add_argument("domainname", type=str, default=None, help="Optional, domainname")
        self.parser.add_argument("username", type=str, default=None, help="Optional, username")
        self.parser.add_argument("password", type=str, default=None, help="Optional, password")
        self.parser.add_argument("securitydomain", type=str, default='Native', help="Optional, securitydomain")
        self.parser.add_argument("resiliencetimeout", type=int, default=None, help="Optional, resiliencetimeout")

        self.parser.add_argument("RT",
                                 type=str,
                                 default="JSON",
                                 help="Return Type(JSON|PROTOBUF)")

    def get(self):
        parameters_list = []
        for i in self.parser.args:
            parameters_dict = {}
            parameters_dict.update({"name": i.name, "help": i.help, "default": i.default})
            parameters_list.append(parameters_dict)
        return {"Usages": parameters_list}

    def post(self):
        args = self.parser.parse_args()
        mainLogger.debug("## args =  {0}".format(args))
        if is_none(args.get("servicename")):
            raise MissingRequiredParametersException(" servicename  are/is requried")
        # return serilization type
        ret_type = args.get("RT")
        if ret_type is None:
            ret_type = "JSON"

        current_node_envs = get_current_node_infa_envs()
        os.environ.update(current_node_envs)
        mainLogger.debug("environment variables is {0}".format(current_node_envs))
        args.pop("RT")

        res = listApplications(**args)
        mainLogger.debug(res)
        stdout = str(res.stdout)
        if ret_type.upper() == "PROTOBUF":
            proto_resp = infaCliResponse_pb2.InfaCliResponse()
            proto_resp.retcode = res.retcode
            proto_resp.stdout = stdout
            res = proto_resp.SerializeToString()
            mainLogger.debug("protobuf: the result is {0}".format(res))
            content_type = Config.PREDEFINED_CONTENT_TYPES.get("PROTOBUF")
        else:
            output_dict = {"retcode": res.retcode,
                           "stdout": stdout
                           }
            res = json.dumps(output_dict)
            content_type = Config.PREDEFINED_CONTENT_TYPES.get("JSON")
        response = make_response(res)
        response.headers["Content-Type"] = content_type
        return response


class ListApplicationObjects(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("servicename", type=str, help="Required")
        self.parser.add_argument("application", type=str, help="Required")
        self.parser.add_argument("domainname", type=str, default=None, help="Optional, domainname")
        self.parser.add_argument("domainaddress", type=str, default=None, help="Optional, domainaddress")
        self.parser.add_argument("username", type=str, default=None, help="Optional, username")
        self.parser.add_argument("password", type=str, default=None, help="Optional, password")
        self.parser.add_argument("securitydomain", type=str, default='Native', help="Optional, securitydomain")
        self.parser.add_argument("resiliencetimeout", type=int, default=None, help="Optional, resiliencetimeout")
        self.parser.add_argument("objecttype", type=str, default=None, help="Optional, objecttype")
        self.parser.add_argument("listobjecttype", type=bool, default=False, help="Optional, listobjecttype")
        self.parser.add_argument("pagesize", type=int, default=None, help="Optional, pagesize")
        self.parser.add_argument("pageindex", type=int, default=None, help="Optional, pageindex")

        self.parser.add_argument("RT",
                                 type=str,
                                 default="JSON",
                                 help="Return Type(JSON|PROTOBUF)")

    def get(self):
        parameters_list = []
        for i in self.parser.args:
            parameters_dict = {}
            parameters_dict.update({"name": i.name, "help": i.help, "default": i.default})
            parameters_list.append(parameters_dict)
        return {"Usages": parameters_list}

    def post(self):
        args = self.parser.parse_args()
        mainLogger.debug("## args =  {0}".format(args))
        if is_none(args.get("servicename")) or is_none(args.get("application")):
            raise MissingRequiredParametersException(" servicename and  application  are/is requried")
        # return serilization type
        ret_type = args.get("RT")
        if ret_type is None:
            ret_type = "JSON"

        # current_node_envs = infa_env.get_envs(current_node.id)  # type: dict
        current_node_envs = get_current_node_infa_envs()
        os.environ.update(current_node_envs)
        mainLogger.debug("environment variables is {0}".format(current_node_envs))
        args.pop("RT")

        res = listApplicationObjects(**args)
        mainLogger.debug(res)
        stdout = str(res.stdout)
        if ret_type.upper() == "PROTOBUF":
            proto_resp = infaCliResponse_pb2.InfaCliResponse()
            proto_resp.retcode = res.retcode
            proto_resp.stdout = stdout
            res = proto_resp.SerializeToString()
            mainLogger.debug("protobuf: the result is {0}".format(res))
            content_type = Config.PREDEFINED_CONTENT_TYPES.get("PROTOBUF")
        else:
            output_dict = {"retcode": res.retcode,
                           "stdout": stdout
                           }
            res = json.dumps(output_dict)
            content_type = Config.PREDEFINED_CONTENT_TYPES.get("JSON")
        response = make_response(res)
        response.headers["Content-Type"] = content_type
        return response


class StopBlazeService(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("ServiceName", type=str, help="Required")
        self.parser.add_argument("HadoopConnection", type=str, help="Required")
        self.parser.add_argument("DomainName", type=str, default=None,
                                 help="Optional, Optional, if it's set the INFA_DEFAULT_DOMAIN")
        self.parser.add_argument("UserName", type=str, default=None,
                                 help="Optional, Optional, if it's set the INFA_DEFAULT_DOMAIN_USER")
        self.parser.add_argument("Password", type=str, default=None,
                                 help="Optional, Optional, if it's set the INFA_DEFAULT_DOMAIN_PASSWORD")
        self.parser.add_argument("SecurityDomain", type=str, default=None,
                                 help="Optional, Optional, if it's set the INFA_DEFAULT_SECURITY_DOMAIN")
        self.parser.add_argument("ResilienceTimeout", type=str, default=None,
                                 help="Optional, Optional, if it's set the INFA_CLIENT_RESILIENCE_TIMEOUT")

        self.parser.add_argument("RT",
                                 type=str,
                                 default="JSON",
                                 help="Return Type(JSON|PROTOBUF)")

    def get(self):
        parameters_list = []
        for i in self.parser.args:
            parameters_dict = {}
            parameters_dict.update({"name": i.name, "help": i.help, "default": i.default})
            parameters_list.append(parameters_dict)
        return {"Usages": parameters_list}

    def post(self):
        args = self.parser.parse_args()
        mainLogger.debug("## args =  {0}".format(args))
        if is_none(args.get("ServiceName")) or is_none(args.get("HadoopConnection")):
            raise MissingRequiredParametersException(" ServiceName and  HadoopConnection  are/is requried")
        # return serilization type
        ret_type = args.get("RT")
        if ret_type is None:
            ret_type = "JSON"

        # current_node_envs = infa_env.get_envs(current_node.id)  # type: dict
        current_node_envs = get_current_node_infa_envs()
        os.environ.update(current_node_envs)
        mainLogger.debug("environment variables is {0}".format(current_node_envs))
        args.pop("RT")

        res = stopBlazeService(**args)
        mainLogger.debug(res)
        stdout = str(res.stdout)
        if ret_type.upper() == "PROTOBUF":
            proto_resp = infaCliResponse_pb2.InfaCliResponse()
            proto_resp.retcode = res.retcode
            proto_resp.stdout = stdout
            res = proto_resp.SerializeToString()
            mainLogger.debug("protobuf: the result is {0}".format(res))
            content_type = Config.PREDEFINED_CONTENT_TYPES.get("PROTOBUF")
        else:
            output_dict = {"retcode": res.retcode,
                           "stdout": stdout
                           }
            res = json.dumps(output_dict)
            content_type = Config.PREDEFINED_CONTENT_TYPES.get("JSON")
        response = make_response(res)
        response.headers["Content-Type"] = content_type
        return response


class BackupApplication(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("ServiceName", type=str, help="Required")
        self.parser.add_argument("Application", type=str, help="Required")
        self.parser.add_argument("FileName", type=str, help="Required")
        self.parser.add_argument("DomainName", type=str, default=None,
                                 help="Optional, Optional, if it's set the INFA_DEFAULT_DOMAIN")
        self.parser.add_argument("UserName", type=str, default=None,
                                 help="Optional, Optional, if it's set the INFA_DEFAULT_DOMAIN_USER")
        self.parser.add_argument("Password", type=str, default=None,
                                 help="Optional, Optional, if it's set the INFA_DEFAULT_DOMAIN_PASSWORD")
        self.parser.add_argument("SecurityDomain", type=str, default=None,
                                 help="Optional, Optional, if it's set the INFA_DEFAULT_SECURITY_DOMAIN")
        self.parser.add_argument("ResilienceTimeout", type=str, default=None,
                                 help="Optional, Optional, if it's set the INFA_CLIENT_RESILIENCE_TIMEOUT")

        self.parser.add_argument("RT",
                                 type=str,
                                 default="JSON",
                                 help="Return Type(JSON|PROTOBUF)")

    def get(self):
        parameters_list = []
        for i in self.parser.args:
            parameters_dict = {}
            parameters_dict.update({"name": i.name, "help": i.help, "default": i.default})
            parameters_list.append(parameters_dict)
        return {"Usages": parameters_list}

    def post(self):
        args = self.parser.parse_args()
        mainLogger.debug("## args =  {0}".format(args))
        if is_none(args.get("ServiceName")) or is_none(args.get("Application")) or is_none(args.get("FileName")):
            raise MissingRequiredParametersException(" ServiceName and  Application and  FileName  are/is requried")
        # return serilization type
        ret_type = args.get("RT")
        if ret_type is None:
            ret_type = "JSON"

        # current_node_envs = infa_env.get_envs(current_node.id)  # type: dict
        current_node_envs = get_current_node_infa_envs()
        os.environ.update(current_node_envs)
        mainLogger.debug("environment variables is {0}".format(current_node_envs))
        args.pop("RT")

        res = backupApplication(**args)
        mainLogger.debug(res)
        stdout = str(res.stdout)
        if ret_type.upper() == "PROTOBUF":
            proto_resp = infaCliResponse_pb2.InfaCliResponse()
            proto_resp.retcode = res.retcode
            proto_resp.stdout = stdout
            res = proto_resp.SerializeToString()
            mainLogger.debug("protobuf: the result is {0}".format(res))
            content_type = Config.PREDEFINED_CONTENT_TYPES.get("PROTOBUF")
        else:
            output_dict = {"retcode": res.retcode,
                           "stdout": stdout
                           }
            res = json.dumps(output_dict)
            content_type = Config.PREDEFINED_CONTENT_TYPES.get("JSON")
        response = make_response(res)
        response.headers["Content-Type"] = content_type
        return response


class StopApplication(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("ServiceName", type=str, help="Required")
        self.parser.add_argument("Application", type=str, help="Required")
        self.parser.add_argument("DomainName", type=str, default=None,
                                 help="Optional, Optional, if it's set the INFA_DEFAULT_DOMAIN")
        self.parser.add_argument("UserName", type=str, default=None,
                                 help="Optional, Optional, if it's set the INFA_DEFAULT_DOMAIN_USER")
        self.parser.add_argument("Password", type=str, default=None,
                                 help="Optional, Optional, if it's set the INFA_DEFAULT_DOMAIN_PASSWORD")
        self.parser.add_argument("SecurityDomain", type=str, default=None,
                                 help="Optional, Optional, if it's set the INFA_DEFAULT_SECURITY_DOMAIN")
        self.parser.add_argument("ResilienceTimeout", type=str, default=None,
                                 help="Optional, Optional, if it's set the INFA_CLIENT_RESILIENCE_TIMEOUT")

        self.parser.add_argument("RT",
                                 type=str,
                                 default="JSON",
                                 help="Return Type(JSON|PROTOBUF)")

    def get(self):
        parameters_list = []
        for i in self.parser.args:
            parameters_dict = {}
            parameters_dict.update({"name": i.name, "help": i.help, "default": i.default})
            parameters_list.append(parameters_dict)
        return {"Usages": parameters_list}

    def post(self):
        args = self.parser.parse_args()
        mainLogger.debug("## args =  {0}".format(args))
        if is_none(args.get("ServiceName")) or is_none(args.get("Application")):
            raise MissingRequiredParametersException(" ServiceName and  Application  are/is requried")
        # return serilization type
        ret_type = args.get("RT")
        if ret_type is None:
            ret_type = "JSON"

        current_node_envs = get_current_node_infa_envs()
        os.environ.update(current_node_envs)
        mainLogger.debug("environment variables is {0}".format(current_node_envs))
        args.pop("RT")

        res = stopApplication(**args)
        mainLogger.debug(res)
        stdout = str(res.stdout)
        if ret_type.upper() == "PROTOBUF":
            proto_resp = infaCliResponse_pb2.InfaCliResponse()
            proto_resp.retcode = res.retcode
            proto_resp.stdout = stdout
            res = proto_resp.SerializeToString()
            mainLogger.debug("protobuf: the result is {0}".format(res))
            content_type = Config.PREDEFINED_CONTENT_TYPES.get("PROTOBUF")
        else:
            output_dict = {"retcode": res.retcode,
                           "stdout": stdout
                           }
            res = json.dumps(output_dict)
            content_type = Config.PREDEFINED_CONTENT_TYPES.get("JSON")
        response = make_response(res)
        response.headers["Content-Type"] = content_type
        return response


class StartApplication(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("ServiceName", type=str, help="Required")
        self.parser.add_argument("Application", type=str, help="Required")
        self.parser.add_argument("DomainName", type=str, default=None,
                                 help="Optional, Optional, if it's set the INFA_DEFAULT_DOMAIN")
        self.parser.add_argument("UserName", type=str, default=None,
                                 help="Optional, Optional, if it's set the INFA_DEFAULT_DOMAIN_USER")
        self.parser.add_argument("Password", type=str, default=None,
                                 help="Optional, Optional, if it's set the INFA_DEFAULT_DOMAIN_PASSWORD")
        self.parser.add_argument("SecurityDomain", type=str, default=None,
                                 help="Optional, Optional, if it's set the INFA_DEFAULT_SECURITY_DOMAIN")
        self.parser.add_argument("ResilienceTimeout", type=str, default=None,
                                 help="Optional, Optional, if it's set the INFA_CLIENT_RESILIENCE_TIMEOUT")

        self.parser.add_argument("RT",
                                 type=str,
                                 default="JSON",
                                 help="Return Type(JSON|PROTOBUF)")

    def get(self):
        parameters_list = []
        for i in self.parser.args:
            parameters_dict = {}
            parameters_dict.update({"name": i.name, "help": i.help, "default": i.default})
            parameters_list.append(parameters_dict)
        return {"Usages": parameters_list}

    def post(self):
        args = self.parser.parse_args()
        mainLogger.debug("## args =  {0}".format(args))
        if is_none(args.get("ServiceName")) or is_none(args.get("Application")):
            raise MissingRequiredParametersException(" ServiceName and  Application  are/is requried")
        # return serilization type
        ret_type = args.get("RT")
        if ret_type is None:
            ret_type = "JSON"

        # current_node_envs = infa_env.get_envs(current_node.id)  # type: dict
        current_node_envs = get_current_node_infa_envs()
        os.environ.update(current_node_envs)
        mainLogger.debug("environment variables is {0}".format(current_node_envs))
        args.pop("RT")

        res = startApplication(**args)
        mainLogger.debug(res)
        stdout = str(res.stdout)
        if ret_type.upper() == "PROTOBUF":
            proto_resp = infaCliResponse_pb2.InfaCliResponse()
            proto_resp.retcode = res.retcode
            proto_resp.stdout = stdout
            res = proto_resp.SerializeToString()
            mainLogger.debug("protobuf: the result is {0}".format(res))
            content_type = Config.PREDEFINED_CONTENT_TYPES.get("PROTOBUF")
        else:
            output_dict = {"retcode": res.retcode,
                           "stdout": stdout
                           }
            res = json.dumps(output_dict)
            content_type = Config.PREDEFINED_CONTENT_TYPES.get("JSON")
        response = make_response(res)
        response.headers["Content-Type"] = content_type
        return response
