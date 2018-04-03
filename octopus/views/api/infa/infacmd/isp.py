# -*- coding:utf-8 -*-
import json
import os
from datetime import datetime

from flask import Blueprint, make_response, g
from flask_restful import reqparse, Resource

from config import Config
from octopus.common import is_none
from octopus.common.logger import mainLogger
from octopus.database.metadata import get_current_node_infa_envs
from octopus.exceptions import MissingRequiredParametersException
from octopus.infa.infacmd.isp import ping, resetPassword, purgeLog, enableServiceProcess, disableServiceProcess, \
    disableService, enableService, listNodes, listNodeResources, listServiceLevels, listServices, listServiceNodes, \
    listServicePrivileges, getServiceStatus, listLicenses, showLicense, listAllUsers, listConnections, \
    listConnectionOptions, listUserPermissions, listUserPrivileges, listGroupsForUser
from octopus.views.api import infaCliResponse_pb2

infacmd_isp_bp = Blueprint("isp", __name__)


class Ping(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()

        self.parser.add_argument("ServiceName",
                                 type=str,
                                 help='ServiceName, it is _adminconsole if the Administrator Console, or you '
                                      'can use the isp/listServices to list the existing services ')
        self.parser.add_argument("NodeName", type=str, default=None, help="optional, Name of the node")
        self.parser.add_argument("GatewayAddress", type=str, default=None,
                                 help="optional, if you want to ping other domain, you can specify it")
        self.parser.add_argument("ResilienceTimeout", type=int, default=None,
                                 help="Default is 180, or INFA_CLIENT_RESILIENCE_TIMEOUT environment variable")
        self.parser.add_argument("RT",
                                 type=str,
                                 default="JSON",
                                 help="Return Type(JSON|PROTOBUF)")

    def get(self):
        ping_parameters_list = []
        for i in self.parser.args:
            ping_parameters_dict = {}
            ping_parameters_dict.update({"name": i.name, "help": i.help, "default": i.default})
            ping_parameters_list.append(ping_parameters_dict)
        return {"Usages": ping_parameters_list}

    def post(self):
        args = self.parser.parse_args()
        mainLogger.debug("## args =  {0}".format(args))
        if is_none(args.get("ServiceName")):
            raise MissingRequiredParametersException(
                "The ServiceName is required, not the {0}".format(args.get("ServiceName")))

        # return serilization type
        ret_type = args.get("RT")
        if ret_type is None:
            ret_type = "JSON"

        # current_node_envs = infa_env.get_envs(current_node.id)  # type: dict
        current_node_envs = get_current_node_infa_envs()
        os.environ.update(current_node_envs)
        mainLogger.debug("environment variables is {0}".format(current_node_envs))
        args.pop("RT")

        res = ping(**args)
        mainLogger.debug(res)

        if ret_type.upper() == "PROTOBUF":
            proto_resp = infaCliResponse_pb2.InfaCliResponse()
            proto_resp.retcode = res.retcode
            proto_resp.stdout = str(res.stdout)
            res = proto_resp.SerializeToString()
            mainLogger.debug("protobuf: the result is {0}".format(res))
            content_type = Config.PREDEFINED_CONTENT_TYPES.get("PROTOBUF")
        else:
            output_dict = {"retcode": res.retcode,
                           "stdout": str(res.stdout)
                           }
            res = json.dumps(output_dict)
            content_type = Config.PREDEFINED_CONTENT_TYPES.get("JSON")
        response = make_response(res)
        response.headers["Content-Type"] = content_type
        return response


class ResetPassword(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()

        self.parser.add_argument("ResetUserName",
                                 type=str,
                                 help='the ResetUserName ')
        self.parser.add_argument("ResetUserPassword", type=str, default=None, help="the ResetUserPassword")
        self.parser.add_argument("UserName", type=str, default=None,
                                 help="Optional, if it's set the INFA_DEFAULT_DOMAIN_USER")
        self.parser.add_argument("Password", type=str, default=None,
                                 help="Optional, if it's set the INFA_DEFAULT_DOMAIN_PASSWORD")
        self.parser.add_argument("SecurityDomain", type=str, default="Native",
                                 help="Optional, if it's set the INFA_DEFAULT_SECURITY_DOMAIN")
        self.parser.add_argument("DomainName", type=str, default=None,
                                 help="optional, if it's set the INFA_DEFAULT_DOMAIN")
        self.parser.add_argument("Gateway", type=str, default=None,
                                 help="optional")
        self.parser.add_argument("ResilienceTimeout", type=int, default=None,
                                 help="Default is 180, or INFA_CLIENT_RESILIENCE_TIMEOUT environment variable")
        self.parser.add_argument("RT",
                                 type=str,
                                 default="JSON",
                                 help="Return Type(JSON|PROTOBUF)")

    def get(self):
        resetpassword_parameters_list = []
        for i in self.parser.args:
            ping_parameters_dict = {}
            ping_parameters_dict.update({"name": i.name, "help": i.help, "default": i.default})
            resetpassword_parameters_list.append(ping_parameters_dict)
        return {"Usages": resetpassword_parameters_list}

    def post(self):
        args = self.parser.parse_args()
        mainLogger.debug("## args =  {0}".format(args))
        if is_none(args.get("ResetUserName")) or is_none(args.get("ResetUserPassword")):
            raise MissingRequiredParametersException(
                "The ServiceName and ResetUserPassword are required, not the {0} and {1}".format(
                    args.get("ServiceName"), args.get("ResetUserPassword")))

        # return serilization type
        ret_type = args.get("RT")
        if ret_type is None:
            ret_type = "JSON"

        current_node_envs = get_current_node_infa_envs()  # type: dict
        os.environ.update(current_node_envs)
        mainLogger.debug("environment variables is {0}".format(current_node_envs))
        args.pop("RT")

        res = resetPassword(**args)
        mainLogger.debug(res)

        if ret_type.upper() == "PROTOBUF":
            proto_resp = infaCliResponse_pb2.InfaCliResponse()
            proto_resp.retcode = res.retcode
            proto_resp.stdout = str(res.stdout)
            res = proto_resp.SerializeToString()
            mainLogger.debug("protobuf: the result is {0}".format(res))
            content_type = Config.PREDEFINED_CONTENT_TYPES.get("PROTOBUF")
        else:
            output_dict = {"retcode": res.retcode,
                           "stdout": str(res.stdout)
                           }
            res = json.dumps(output_dict)
            content_type = Config.PREDEFINED_CONTENT_TYPES.get("JSON")
        response = make_response(res)
        response.headers["Content-Type"] = content_type
        return response


class PurgeLog(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("BeforeDate",
                                 type=str,
                                 help='BeforeDate, Default is server system time. format: (MM/dd/yyyy|yyyy-MM-dd)')
        self.parser.add_argument("UserName", type=str, default=None,
                                 help="Optional, if it's set the INFA_DEFAULT_DOMAIN_USER")
        self.parser.add_argument("Password", type=str, default=None,
                                 help="Optional, if it's set the INFA_DEFAULT_DOMAIN_PASSWORD")
        self.parser.add_argument("SecurityDomain", type=str, default="Native",
                                 help="Optional, if it's set the INFA_DEFAULT_SECURITY_DOMAIN")
        self.parser.add_argument("Gateway", type=str, default=None,
                                 help="optional")
        self.parser.add_argument("ResilienceTimeout", type=int, default=None,
                                 help="Default is 180, or INFA_CLIENT_RESILIENCE_TIMEOUT environment variable")
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
        if is_none(args.get("BeforeDate")):
            server_now = datetime.now()
            now = server_now.strftime("%m/%d/%Y")
            args.update({"BeforeDate": now})
            mainLogger.debug("The BeforeDate is missing, and now set it to {0}".format(now))

        # return serilization type
        ret_type = args.get("RT")
        if ret_type is None:
            ret_type = "JSON"

        # current_node_envs = infa_env.get_envs(current_node.id)  # type: dict
        current_node_envs = get_current_node_infa_envs()
        os.environ.update(current_node_envs)
        mainLogger.debug("environment variables is {0}".format(current_node_envs))
        args.pop("RT")

        res = purgeLog(**args)
        mainLogger.debug(res)

        if ret_type.upper() == "PROTOBUF":
            proto_resp = infaCliResponse_pb2.InfaCliResponse()
            proto_resp.retcode = res.retcode
            proto_resp.stdout = str(res.stdout)
            res = proto_resp.SerializeToString()
            mainLogger.debug("protobuf: the result is {0}".format(res))
            content_type = Config.PREDEFINED_CONTENT_TYPES.get("PROTOBUF")
        else:
            output_dict = {"retcode": res.retcode,
                           "stdout": str(res.stdout)
                           }
            res = json.dumps(output_dict)
            content_type = Config.PREDEFINED_CONTENT_TYPES.get("JSON")
        response = make_response(res)
        response.headers["Content-Type"] = content_type
        return response


class EnableServiceProcess(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("ServiceName",
                                 type=str,
                                 help='Name of Service')
        self.parser.add_argument("NodeName", type=str, help="the Name of Node")
        self.parser.add_argument("DomainName", type=str, default=None,
                                 help="Optional, if it's set the INFA_DEFAULT_DOMAIN")
        self.parser.add_argument("UserName", type=str, default=None,
                                 help="Optional, if it's set the INFA_DEFAULT_DOMAIN_USER")
        self.parser.add_argument("Password", type=str, default=None,
                                 help="Optional, if it's set the INFA_DEFAULT_DOMAIN_PASSWORD")
        self.parser.add_argument("SecurityDomain", type=str, default="Native",
                                 help="Optional, if it's set the INFA_DEFAULT_SECURITY_DOMAIN")
        self.parser.add_argument("Gateway", type=str, default=None,
                                 help="optional")
        self.parser.add_argument("ResilienceTimeout", type=int, default=None,
                                 help="Default is 180, or INFA_CLIENT_RESILIENCE_TIMEOUT environment variable")
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
        if is_none(args.get("ServiceName")) or is_none(args.get("NodeName")):
            raise MissingRequiredParametersException("The ServiceName and NodeName are required")
        # return serilization type
        ret_type = args.get("RT")
        if ret_type is None:
            ret_type = "JSON"

        current_node_envs = get_current_node_infa_envs()
        os.environ.update(current_node_envs)
        mainLogger.debug("environment variables is {0}".format(current_node_envs))
        args.pop("RT")

        res = enableServiceProcess(**args)
        mainLogger.debug(res)

        if ret_type.upper() == "PROTOBUF":
            proto_resp = infaCliResponse_pb2.InfaCliResponse()
            proto_resp.retcode = res.retcode
            proto_resp.stdout = str(res.stdout)
            res = proto_resp.SerializeToString()
            mainLogger.debug("protobuf: the result is {0}".format(res))
            content_type = Config.PREDEFINED_CONTENT_TYPES.get("PROTOBUF")
        else:
            output_dict = {"retcode": res.retcode,
                           "stdout": str(res.stdout)
                           }
            res = json.dumps(output_dict)
            content_type = Config.PREDEFINED_CONTENT_TYPES.get("JSON")
        response = make_response(res)
        response.headers["Content-Type"] = content_type
        return response


class DisableServiceProcess(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("ServiceName",
                                 type=str,
                                 help='Name of Service')
        self.parser.add_argument("NodeName", type=str, help="the Name of Node")
        self.parser.add_argument("Mode", type=str, default="Complete",
                                 help="Default is Complete. (Complete|Abort|Stop)")
        self.parser.add_argument("DomainName", type=str, default=None,
                                 help="Optional, if it's set the INFA_DEFAULT_DOMAIN")
        self.parser.add_argument("UserName", type=str, default=None,
                                 help="Optional, if it's set the INFA_DEFAULT_DOMAIN_USER")
        self.parser.add_argument("Password", type=str, default=None,
                                 help="Optional, if it's set the INFA_DEFAULT_DOMAIN_PASSWORD")
        self.parser.add_argument("SecurityDomain", type=str, default="Native",
                                 help="Optional, if it's set the INFA_DEFAULT_SECURITY_DOMAIN")
        self.parser.add_argument("Gateway", type=str, default=None,
                                 help="optional")
        self.parser.add_argument("ResilienceTimeout", type=int, default=None,
                                 help="Default is 180, or INFA_CLIENT_RESILIENCE_TIMEOUT environment variable")
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
        if is_none(args.get("ServiceName")) or is_none(args.get("NodeName")):
            raise MissingRequiredParametersException("The ServiceName and NodeName are required")
        # return serilization type
        ret_type = args.get("RT")
        if ret_type is None:
            ret_type = "JSON"

        current_node_envs = get_current_node_infa_envs()
        os.environ.update(current_node_envs)
        mainLogger.debug("environment variables is {0}".format(current_node_envs))
        args.pop("RT")

        res = disableServiceProcess(**args)
        mainLogger.debug(res)

        if ret_type.upper() == "PROTOBUF":
            proto_resp = infaCliResponse_pb2.InfaCliResponse()
            proto_resp.retcode = res.retcode
            proto_resp.stdout = str(res.stdout)
            res = proto_resp.SerializeToString()
            mainLogger.debug("protobuf: the result is {0}".format(res))
            content_type = Config.PREDEFINED_CONTENT_TYPES.get("PROTOBUF")
        else:
            output_dict = {"retcode": res.retcode,
                           "stdout": str(res.stdout)
                           }
            res = json.dumps(output_dict)
            content_type = Config.PREDEFINED_CONTENT_TYPES.get("JSON")
        response = make_response(res)
        response.headers["Content-Type"] = content_type
        return response


class EnableService(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("ServiceName",
                                 type=str,
                                 help='Name of Service')
        self.parser.add_argument("DomainName", type=str, default=None,
                                 help="Optional, if it's set the INFA_DEFAULT_DOMAIN")
        self.parser.add_argument("UserName", type=str, default=None,
                                 help="Optional, if it's set the INFA_DEFAULT_DOMAIN_USER")
        self.parser.add_argument("Password", type=str, default=None,
                                 help="Optional, if it's set the INFA_DEFAULT_DOMAIN_PASSWORD")
        self.parser.add_argument("SecurityDomain", type=str, default="Native",
                                 help="Optional, if it's set the INFA_DEFAULT_SECURITY_DOMAIN")
        self.parser.add_argument("Gateway", type=str, default=None,
                                 help="optional")
        self.parser.add_argument("ResilienceTimeout", type=int, default=None,
                                 help="Default is 180, or INFA_CLIENT_RESILIENCE_TIMEOUT environment variable")
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
        if is_none(args.get("ServiceName")):
            raise MissingRequiredParametersException("The ServiceName is required")
        # return serilization type
        ret_type = args.get("RT")
        if ret_type is None:
            ret_type = "JSON"

        current_node_envs = get_current_node_infa_envs()
        os.environ.update(current_node_envs)
        mainLogger.debug("environment variables is {0}".format(current_node_envs))
        args.pop("RT")

        res = enableService(**args)
        mainLogger.debug(res)

        if ret_type.upper() == "PROTOBUF":
            proto_resp = infaCliResponse_pb2.InfaCliResponse()
            proto_resp.retcode = res.retcode
            proto_resp.stdout = str(res.stdout)
            res = proto_resp.SerializeToString()
            mainLogger.debug("protobuf: the result is {0}".format(res))
            content_type = Config.PREDEFINED_CONTENT_TYPES.get("PROTOBUF")
        else:
            output_dict = {"retcode": res.retcode,
                           "stdout": str(res.stdout)
                           }
            res = json.dumps(output_dict)
            content_type = Config.PREDEFINED_CONTENT_TYPES.get("JSON")
        response = make_response(res)
        response.headers["Content-Type"] = content_type
        return response


class DisableService(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("ServiceName",
                                 type=str,
                                 help='Name of Service')
        self.parser.add_argument("Mode", type=str, default="Complete",
                                 help="Default is Complete. (Complete|Abort|Stop)")
        self.parser.add_argument("DomainName", type=str, default=None,
                                 help="Optional, if it's set the INFA_DEFAULT_DOMAIN")
        self.parser.add_argument("UserName", type=str, default=None,
                                 help="Optional, if it's set the INFA_DEFAULT_DOMAIN_USER")
        self.parser.add_argument("Password", type=str, default=None,
                                 help="Optional, if it's set the INFA_DEFAULT_DOMAIN_PASSWORD")
        self.parser.add_argument("SecurityDomain", type=str, default="Native",
                                 help="Optional, if it's set the INFA_DEFAULT_SECURITY_DOMAIN")
        self.parser.add_argument("Gateway", type=str, default=None,
                                 help="optional")
        self.parser.add_argument("ResilienceTimeout", type=int, default=None,
                                 help="Default is 180, or INFA_CLIENT_RESILIENCE_TIMEOUT environment variable")
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
        if is_none(args.get("ServiceName")):
            raise MissingRequiredParametersException("The ServiceName is required")
        # return serilization type
        ret_type = args.get("RT")
        if ret_type is None:
            ret_type = "JSON"

        # current_node_envs = infa_env.get_envs(current_node.id)  # type: dict
        current_node_envs = get_current_node_infa_envs()
        os.environ.update(current_node_envs)
        mainLogger.debug("environment variables is {0}".format(current_node_envs))
        args.pop("RT")

        res = disableService(**args)
        mainLogger.debug(res)

        if ret_type.upper() == "PROTOBUF":
            proto_resp = infaCliResponse_pb2.InfaCliResponse()
            proto_resp.retcode = res.retcode
            proto_resp.stdout = str(res.stdout)
            res = proto_resp.SerializeToString()
            mainLogger.debug("protobuf: the result is {0}".format(res))
            content_type = Config.PREDEFINED_CONTENT_TYPES.get("PROTOBUF")
        else:
            output_dict = {"retcode": res.retcode,
                           "stdout": str(res.stdout)
                           }
            res = json.dumps(output_dict)
            content_type = Config.PREDEFINED_CONTENT_TYPES.get("JSON")
        response = make_response(res)
        response.headers["Content-Type"] = content_type
        return response


class ListNodes(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("DomainName", type=str, default=None,
                                 help="Optional, if it's set the INFA_DEFAULT_DOMAIN")
        self.parser.add_argument("UserName", type=str, default=None,
                                 help="Optional, if it's set the INFA_DEFAULT_DOMAIN_USER")
        self.parser.add_argument("Password", type=str, default=None,
                                 help="Optional, if it's set the INFA_DEFAULT_DOMAIN_PASSWORD")
        self.parser.add_argument("SecurityDomain", type=str, default="Native",
                                 help="Optional, if it's set the INFA_DEFAULT_SECURITY_DOMAIN")
        self.parser.add_argument("Gateway", type=str, default=None,
                                 help="optional")
        self.parser.add_argument("ResilienceTimeout", type=int, default=None,
                                 help="Default is 180, or INFA_CLIENT_RESILIENCE_TIMEOUT environment variable")
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

        # return serilization type
        ret_type = args.get("RT")
        if ret_type is None:
            ret_type = "JSON"

        # current_node_envs = infa_env.get_envs(current_node.id)  # type: dict
        current_node_envs = get_current_node_infa_envs()
        os.environ.update(current_node_envs)
        mainLogger.debug("environment variables is {0}".format(current_node_envs))
        args.pop("RT")

        res = listNodes(**args)
        mainLogger.debug(res)

        if ret_type.upper() == "PROTOBUF":
            proto_resp = infaCliResponse_pb2.InfaCliResponse()
            proto_resp.retcode = res.retcode
            proto_resp.stdout = str(res.stdout)
            res = proto_resp.SerializeToString()
            mainLogger.debug("protobuf: the result is {0}".format(res))
            content_type = Config.PREDEFINED_CONTENT_TYPES.get("PROTOBUF")
        else:
            output_dict = {"retcode": res.retcode,
                           "stdout": str(res.stdout)
                           }
            res = json.dumps(output_dict)
            content_type = Config.PREDEFINED_CONTENT_TYPES.get("JSON")
        response = make_response(res)
        response.headers["Content-Type"] = content_type
        return response


class ListNodeResources(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("NodeName",
                                 type=str,
                                 help='Name of Node')
        self.parser.add_argument("ResourceCategory", type=str, default="PCIS",
                                 help="Default is PCIS. (PCIS|DIS)")
        self.parser.add_argument("DomainName", type=str, default=None,
                                 help="Optional, if it's set the INFA_DEFAULT_DOMAIN")
        self.parser.add_argument("UserName", type=str, default=None,
                                 help="Optional, if it's set the INFA_DEFAULT_DOMAIN_USER")
        self.parser.add_argument("Password", type=str, default=None,
                                 help="Optional, if it's set the INFA_DEFAULT_DOMAIN_PASSWORD")
        self.parser.add_argument("SecurityDomain", type=str, default="Native",
                                 help="Optional, if it's set the INFA_DEFAULT_SECURITY_DOMAIN")
        self.parser.add_argument("Gateway", type=str, default=None,
                                 help="optional")
        self.parser.add_argument("ResilienceTimeout", type=int, default=None,
                                 help="Default is 180, or INFA_CLIENT_RESILIENCE_TIMEOUT environment variable")
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
        if is_none(args.get("NodeName")):
            raise MissingRequiredParametersException("The NodeName is required")
        # return serilization type
        ret_type = args.get("RT")
        if ret_type is None:
            ret_type = "JSON"

        # current_node_envs = infa_env.get_envs(current_node.id)  # type: dict
        current_node_envs = get_current_node_infa_envs()
        os.environ.update(current_node_envs)
        mainLogger.debug("environment variables is {0}".format(current_node_envs))
        args.pop("RT")

        res = listNodeResources(**args)
        mainLogger.debug(res)

        if ret_type.upper() == "PROTOBUF":
            proto_resp = infaCliResponse_pb2.InfaCliResponse()
            proto_resp.retcode = res.retcode
            proto_resp.stdout = str(res.stdout)
            res = proto_resp.SerializeToString()
            mainLogger.debug("protobuf: the result is {0}".format(res))
            content_type = Config.PREDEFINED_CONTENT_TYPES.get("PROTOBUF")
        else:
            output_dict = {"retcode": res.retcode,
                           "stdout": str(res.stdout)
                           }
            res = json.dumps(output_dict)
            content_type = Config.PREDEFINED_CONTENT_TYPES.get("JSON")
        response = make_response(res)
        response.headers["Content-Type"] = content_type
        return response


class ListServiceLevels(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("DomainName", type=str, default=None,
                                 help="Optional, Optional, if it's set the INFA_DEFAULT_DOMAIN")
        self.parser.add_argument("UserName", type=str, default=None,
                                 help="Optional, Optional, if it's set the INFA_DEFAULT_DOMAIN_USER")
        self.parser.add_argument("Password", type=str, default=None,
                                 help="Optional, Optional, if it's set the INFA_DEFAULT_DOMAIN_PASSWORD")
        self.parser.add_argument("SecurityDomain", type=str, default=None,
                                 help="Optional, Optional, if it's set the INFA_DEFAULT_SECURITY_DOMAIN")
        self.parser.add_argument("Gateway", type=str, default=None, help="Optional, Gateway")
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

        # return serilization type
        ret_type = args.get("RT")
        if ret_type is None:
            ret_type = "JSON"

        # current_node_envs = infa_env.get_envs(current_node.id)  # type: dict
        current_node_envs = get_current_node_infa_envs()
        os.environ.update(current_node_envs)
        mainLogger.debug("environment variables is {0}".format(current_node_envs))
        args.pop("RT")

        res = listServiceLevels(**args)
        mainLogger.debug(res)

        if ret_type.upper() == "PROTOBUF":
            proto_resp = infaCliResponse_pb2.InfaCliResponse()
            proto_resp.retcode = res.retcode
            proto_resp.stdout = str(res.stdout)
            res = proto_resp.SerializeToString()
            mainLogger.debug("protobuf: the result is {0}".format(res))
            content_type = Config.PREDEFINED_CONTENT_TYPES.get("PROTOBUF")
        else:
            output_dict = {"retcode": res.retcode,
                           "stdout": str(res.stdout)
                           }
            res = json.dumps(output_dict)
            content_type = Config.PREDEFINED_CONTENT_TYPES.get("JSON")
        response = make_response(res)
        response.headers["Content-Type"] = content_type
        return response


class ListServices(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("DomainName", type=str, default=None,
                                 help="Optional, Optional, if it's set the INFA_DEFAULT_DOMAIN")
        self.parser.add_argument("UserName", type=str, default=None,
                                 help="Optional, Optional, if it's set the INFA_DEFAULT_DOMAIN_USER")
        self.parser.add_argument("Password", type=str, default=None,
                                 help="Optional, Optional, if it's set the INFA_DEFAULT_DOMAIN_PASSWORD")
        self.parser.add_argument("SecurityDomain", type=str, default=None,
                                 help="Optional, Optional, if it's set the INFA_DEFAULT_SECURITY_DOMAIN")
        self.parser.add_argument("Gateway", type=str, default=None, help="Optional, Gateway")
        self.parser.add_argument("ResilienceTimeout", type=str, default=None,
                                 help="Optional, Optional, if it's set the INFA_CLIENT_RESILIENCE_TIMEOUT")
        self.parser.add_argument("ServiceType", type=str, default=None, help="Optional, ServiceType")
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

        # return serilization type
        ret_type = args.get("RT")
        if ret_type is None:
            ret_type = "JSON"

        # current_node_envs = infa_env.get_envs(current_node.id)  # type: dict
        current_node_envs = get_current_node_infa_envs()
        os.environ.update(current_node_envs)
        mainLogger.debug("environment variables is {0}".format(current_node_envs))
        args.pop("RT")

        res = listServices(**args)
        mainLogger.debug(res)

        if ret_type.upper() == "PROTOBUF":
            proto_resp = infaCliResponse_pb2.InfaCliResponse()
            proto_resp.retcode = res.retcode
            proto_resp.stdout = str(res.stdout)
            res = proto_resp.SerializeToString()
            mainLogger.debug("protobuf: the result is {0}".format(res))
            content_type = Config.PREDEFINED_CONTENT_TYPES.get("PROTOBUF")
        else:
            output_dict = {"retcode": res.retcode,
                           "stdout": str(res.stdout)
                           }
            res = json.dumps(output_dict)
            content_type = Config.PREDEFINED_CONTENT_TYPES.get("JSON")
        response = make_response(res)
        response.headers["Content-Type"] = content_type
        return response


class ListServiceNodes(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("ServiceName", type=str, help="Required")
        self.parser.add_argument("DomainName", type=str, default=None,
                                 help="Optional, Optional, if it's set the INFA_DEFAULT_DOMAIN")
        self.parser.add_argument("UserName", type=str, default=None,
                                 help="Optional, Optional, if it's set the INFA_DEFAULT_DOMAIN_USER")
        self.parser.add_argument("Password", type=str, default=None,
                                 help="Optional, Optional, if it's set the INFA_DEFAULT_DOMAIN_PASSWORD")
        self.parser.add_argument("SecurityDomain", type=str, default=None,
                                 help="Optional, Optional, if it's set the INFA_DEFAULT_SECURITY_DOMAIN")
        self.parser.add_argument("Gateway", type=str, default=None, help="Optional, Gateway")
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
        if is_none(args.get("ServiceName")):
            raise MissingRequiredParametersException(" ServiceName  are/is requried")
        # return serilization type
        ret_type = args.get("RT")
        if ret_type is None:
            ret_type = "JSON"

        # current_node_envs = infa_env.get_envs(current_node.id)  # type: dict
        current_node_envs = get_current_node_infa_envs()
        os.environ.update(current_node_envs)
        mainLogger.debug("environment variables is {0}".format(current_node_envs))
        args.pop("RT")

        res = listServiceNodes(**args)
        mainLogger.debug(res)

        if ret_type.upper() == "PROTOBUF":
            proto_resp = infaCliResponse_pb2.InfaCliResponse()
            proto_resp.retcode = res.retcode
            proto_resp.stdout = str(res.stdout)
            res = proto_resp.SerializeToString()
            mainLogger.debug("protobuf: the result is {0}".format(res))
            content_type = Config.PREDEFINED_CONTENT_TYPES.get("PROTOBUF")
        else:
            output_dict = {"retcode": res.retcode,
                           "stdout": str(res.stdout)
                           }
            res = json.dumps(output_dict)
            content_type = Config.PREDEFINED_CONTENT_TYPES.get("JSON")
        response = make_response(res)
        response.headers["Content-Type"] = content_type
        return response


class ListServicePrivileges(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("DomainName", type=str, default=None,
                                 help="Optional, Optional, if it's set the INFA_DEFAULT_DOMAIN")
        self.parser.add_argument("UserName", type=str, default=None,
                                 help="Optional, Optional, if it's set the INFA_DEFAULT_DOMAIN_USER")
        self.parser.add_argument("Password", type=str, default=None,
                                 help="Optional, Optional, if it's set the INFA_DEFAULT_DOMAIN_PASSWORD")
        self.parser.add_argument("SecurityDomain", type=str, default=None,
                                 help="Optional, Optional, if it's set the INFA_DEFAULT_SECURITY_DOMAIN")
        self.parser.add_argument("Gateway", type=str, default=None, help="Optional, Gateway")
        self.parser.add_argument("ResilienceTimeout", type=str, default=None,
                                 help="Optional, Optional, if it's set the INFA_CLIENT_RESILIENCE_TIMEOUT")
        self.parser.add_argument("ServiceType", type=str, default=None, help="Optional, ServiceType")
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
        # return serilization type
        ret_type = args.get("RT")
        if ret_type is None:
            ret_type = "JSON"

        # current_node_envs = infa_env.get_envs(current_node.id)  # type: dict
        current_node_envs = get_current_node_infa_envs()
        os.environ.update(current_node_envs)
        mainLogger.debug("environment variables is {0}".format(current_node_envs))
        args.pop("RT")

        res = listServicePrivileges(**args)
        mainLogger.debug(res)

        if ret_type.upper() == "PROTOBUF":
            proto_resp = infaCliResponse_pb2.InfaCliResponse()
            proto_resp.retcode = res.retcode
            proto_resp.stdout = str(res.stdout)
            res = proto_resp.SerializeToString()
            mainLogger.debug("protobuf: the result is {0}".format(res))
            content_type = Config.PREDEFINED_CONTENT_TYPES.get("PROTOBUF")
        else:
            output_dict = {"retcode": res.retcode,
                           "stdout": str(res.stdout)
                           }
            res = json.dumps(output_dict)
            content_type = Config.PREDEFINED_CONTENT_TYPES.get("JSON")
        response = make_response(res)
        response.headers["Content-Type"] = content_type
        return response


class GetServiceStatus(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("ServiceName", type=str, help="Required")
        self.parser.add_argument("DomainName", type=str, default=None,
                                 help="Optional, Optional, if it's set the INFA_DEFAULT_DOMAIN")
        self.parser.add_argument("UserName", type=str, default=None,
                                 help="Optional, Optional, if it's set the INFA_DEFAULT_DOMAIN_USER")
        self.parser.add_argument("Password", type=str, default=None,
                                 help="Optional, Optional, if it's set the INFA_DEFAULT_DOMAIN_PASSWORD")
        self.parser.add_argument("SecurityDomain", type=str, default=None,
                                 help="Optional, Optional, if it's set the INFA_DEFAULT_SECURITY_DOMAIN")
        self.parser.add_argument("Gateway", type=str, default=None, help="Optional, Gateway")
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
        if is_none(args.get("ServiceName")):
            raise MissingRequiredParametersException(" ServiceName  are/is requried")
        # return serilization type
        ret_type = args.get("RT")
        if ret_type is None:
            ret_type = "JSON"

        # current_node_envs = infa_env.get_envs(current_node.id)  # type: dict
        current_node_envs = get_current_node_infa_envs()
        os.environ.update(current_node_envs)
        mainLogger.debug("environment variables is {0}".format(current_node_envs))
        args.pop("RT")

        res = getServiceStatus(**args)
        mainLogger.debug(res)

        if ret_type.upper() == "PROTOBUF":
            proto_resp = infaCliResponse_pb2.InfaCliResponse()
            proto_resp.retcode = res.retcode
            proto_resp.stdout = str(res.stdout)
            res = proto_resp.SerializeToString()
            mainLogger.debug("protobuf: the result is {0}".format(res))
            content_type = Config.PREDEFINED_CONTENT_TYPES.get("PROTOBUF")
        else:
            output_dict = {"retcode": res.retcode,
                           "stdout": str(res.stdout)
                           }
            res = json.dumps(output_dict)
            content_type = Config.PREDEFINED_CONTENT_TYPES.get("JSON")
        response = make_response(res)
        response.headers["Content-Type"] = content_type
        return response


class ListLicenses(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("DomainName", type=str, default=None,
                                 help="Optional, Optional, if it's set the INFA_DEFAULT_DOMAIN")
        self.parser.add_argument("UserName", type=str, default=None,
                                 help="Optional, Optional, if it's set the INFA_DEFAULT_DOMAIN_USER")
        self.parser.add_argument("Password", type=str, default=None,
                                 help="Optional, Optional, if it's set the INFA_DEFAULT_DOMAIN_PASSWORD")
        self.parser.add_argument("SecurityDomain", type=str, default=None,
                                 help="Optional, Optional, if it's set the INFA_DEFAULT_SECURITY_DOMAIN")
        self.parser.add_argument("Gateway", type=str, default=None, help="Optional, Gateway")
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

        # return serilization type
        ret_type = args.get("RT")
        if ret_type is None:
            ret_type = "JSON"

        current_node_envs = get_current_node_infa_envs()
        os.environ.update(current_node_envs)
        mainLogger.debug("environment variables is {0}".format(current_node_envs))
        args.pop("RT")

        res = listLicenses(**args)
        mainLogger.debug(res)

        if ret_type.upper() == "PROTOBUF":
            proto_resp = infaCliResponse_pb2.InfaCliResponse()
            proto_resp.retcode = res.retcode
            proto_resp.stdout = str(res.stdout)
            res = proto_resp.SerializeToString()
            mainLogger.debug("protobuf: the result is {0}".format(res))
            content_type = Config.PREDEFINED_CONTENT_TYPES.get("PROTOBUF")
        else:
            output_dict = {"retcode": res.retcode,
                           "stdout": str(res.stdout)
                           }
            res = json.dumps(output_dict)
            content_type = Config.PREDEFINED_CONTENT_TYPES.get("JSON")
        response = make_response(res)
        response.headers["Content-Type"] = content_type
        return response


class ShowLicense(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("LicenseName", type=str, help="Required")
        self.parser.add_argument("DomainName", type=str, default=None,
                                 help="Optional, Optional, if it's set the INFA_DEFAULT_DOMAIN")
        self.parser.add_argument("UserName", type=str, default=None,
                                 help="Optional, Optional, if it's set the INFA_DEFAULT_DOMAIN_USER")
        self.parser.add_argument("Password", type=str, default=None,
                                 help="Optional, Optional, if it's set the INFA_DEFAULT_DOMAIN_PASSWORD")
        self.parser.add_argument("SecurityDomain", type=str, default=None,
                                 help="Optional, Optional, if it's set the INFA_DEFAULT_SECURITY_DOMAIN")
        self.parser.add_argument("Gateway", type=str, default=None, help="Optional, Gateway")
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
        if is_none(args.get("LicenseName")):
            raise MissingRequiredParametersException(" LicenseName  are/is requried")
        # return serilization type
        ret_type = args.get("RT")
        if ret_type is None:
            ret_type = "JSON"

        # current_node_envs = infa_env.get_envs(current_node.id)  # type: dict
        current_node_envs = get_current_node_infa_envs()
        os.environ.update(current_node_envs)
        mainLogger.debug("environment variables is {0}".format(current_node_envs))
        args.pop("RT")

        res = showLicense(**args)
        mainLogger.debug(res)

        if ret_type.upper() == "PROTOBUF":
            proto_resp = infaCliResponse_pb2.InfaCliResponse()
            proto_resp.retcode = res.retcode
            proto_resp.stdout = str(res.stdout)
            res = proto_resp.SerializeToString()
            mainLogger.debug("protobuf: the result is {0}".format(res))
            content_type = Config.PREDEFINED_CONTENT_TYPES.get("PROTOBUF")
        else:
            output_dict = {"retcode": res.retcode,
                           "stdout": str(res.stdout)
                           }
            res = json.dumps(output_dict)
            content_type = Config.PREDEFINED_CONTENT_TYPES.get("JSON")
        response = make_response(res)
        response.headers["Content-Type"] = content_type
        return response


class ListAllUsers(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("DomainName", type=str, default=None,
                                 help="Optional, Optional, if it's set the INFA_DEFAULT_DOMAIN")
        self.parser.add_argument("UserName", type=str, default=None,
                                 help="Optional, Optional, if it's set the INFA_DEFAULT_DOMAIN_USER")
        self.parser.add_argument("Password", type=str, default=None,
                                 help="Optional, Optional, if it's set the INFA_DEFAULT_DOMAIN_PASSWORD")
        self.parser.add_argument("SecurityDomain", type=str, default=None,
                                 help="Optional, Optional, if it's set the INFA_DEFAULT_SECURITY_DOMAIN")
        self.parser.add_argument("Gateway", type=str, default=None, help="Optional, Gateway")
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

        # return serilization type
        ret_type = args.get("RT")
        if ret_type is None:
            ret_type = "JSON"

        # current_node_envs = infa_env.get_envs(current_node.id)  # type: dict
        current_node_envs = get_current_node_infa_envs()
        os.environ.update(current_node_envs)
        mainLogger.debug("environment variables is {0}".format(current_node_envs))
        args.pop("RT")

        res = listAllUsers(**args)
        mainLogger.debug(res)

        if ret_type.upper() == "PROTOBUF":
            proto_resp = infaCliResponse_pb2.InfaCliResponse()
            proto_resp.retcode = res.retcode
            proto_resp.stdout = str(res.stdout)
            res = proto_resp.SerializeToString()
            mainLogger.debug("protobuf: the result is {0}".format(res))
            content_type = Config.PREDEFINED_CONTENT_TYPES.get("PROTOBUF")
        else:
            output_dict = {"retcode": res.retcode,
                           "stdout": str(res.stdout)
                           }
            res = json.dumps(output_dict)
            content_type = Config.PREDEFINED_CONTENT_TYPES.get("JSON")
        response = make_response(res)
        response.headers["Content-Type"] = content_type
        return response


class ListConnections(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("DomainName", type=str, default=None,
                                 help="Optional, Optional, if it's set the INFA_DEFAULT_DOMAIN")
        self.parser.add_argument("UserName", type=str, default=None,
                                 help="Optional, Optional, if it's set the INFA_DEFAULT_DOMAIN_USER")
        self.parser.add_argument("Password", type=str, default=None,
                                 help="Optional, Optional, if it's set the INFA_DEFAULT_DOMAIN_PASSWORD")
        self.parser.add_argument("ConnectionType", type=str, default=None, help="Optional, ConnectionType")
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

        # return serilization type
        ret_type = args.get("RT")
        if ret_type is None:
            ret_type = "JSON"

        # current_node_envs = infa_env.get_envs(current_node.id)  # type: dict
        current_node_envs = get_current_node_infa_envs()
        os.environ.update(current_node_envs)
        mainLogger.debug("environment variables is {0}".format(current_node_envs))
        args.pop("RT")

        res = listConnections(**args)
        mainLogger.debug(res)

        if ret_type.upper() == "PROTOBUF":
            proto_resp = infaCliResponse_pb2.InfaCliResponse()
            proto_resp.retcode = res.retcode
            proto_resp.stdout = str(res.stdout)
            res = proto_resp.SerializeToString()
            mainLogger.debug("protobuf: the result is {0}".format(res))
            content_type = Config.PREDEFINED_CONTENT_TYPES.get("PROTOBUF")
        else:
            output_dict = {"retcode": res.retcode,
                           "stdout": str(res.stdout)
                           }
            res = json.dumps(output_dict)
            content_type = Config.PREDEFINED_CONTENT_TYPES.get("JSON")
        response = make_response(res)
        response.headers["Content-Type"] = content_type
        return response


class ListConnectionOptions(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("ConnectionName", type=str, help="Required")
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
        if is_none(args.get("ConnectionName")):
            raise MissingRequiredParametersException(" ConnectionName  are/is requried")
        # return serilization type
        ret_type = args.get("RT")
        if ret_type is None:
            ret_type = "JSON"

        # current_node_envs = infa_env.get_envs(current_node.id)  # type: dict
        current_node_envs = get_current_node_infa_envs()
        os.environ.update(current_node_envs)
        mainLogger.debug("environment variables is {0}".format(current_node_envs))
        args.pop("RT")

        res = listConnectionOptions(**args)
        mainLogger.debug(res)

        if ret_type.upper() == "PROTOBUF":
            proto_resp = infaCliResponse_pb2.InfaCliResponse()
            proto_resp.retcode = res.retcode
            proto_resp.stdout = str(res.stdout)
            res = proto_resp.SerializeToString()
            mainLogger.debug("protobuf: the result is {0}".format(res))
            content_type = Config.PREDEFINED_CONTENT_TYPES.get("PROTOBUF")
        else:
            output_dict = {"retcode": res.retcode,
                           "stdout": str(res.stdout)
                           }
            res = json.dumps(output_dict)
            content_type = Config.PREDEFINED_CONTENT_TYPES.get("JSON")
        response = make_response(res)
        response.headers["Content-Type"] = content_type
        return response


class ListUserPermissions(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("ExistingUserName", type=str, help="Required")
        self.parser.add_argument("ExistingUserSecurityDomain", type=str, default='Native',
                                 help="Optional, ExistingUserSecurityDomain")
        self.parser.add_argument("ObjectType", type=str, default=None, help="Optional, ObjectType")
        self.parser.add_argument("DomainName", type=str, default=None,
                                 help="Optional, Optional, if it's set the INFA_DEFAULT_DOMAIN")
        self.parser.add_argument("UserName", type=str, default=None,
                                 help="Optional, Optional, if it's set the INFA_DEFAULT_DOMAIN_USER")
        self.parser.add_argument("Password", type=str, default=None,
                                 help="Optional, Optional, if it's set the INFA_DEFAULT_DOMAIN_PASSWORD")
        self.parser.add_argument("SecurityDomain", type=str, default=None,
                                 help="Optional, Optional, if it's set the INFA_DEFAULT_SECURITY_DOMAIN")
        self.parser.add_argument("Gateway", type=str, default=None, help="Optional, Gateway")
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
        if is_none(args.get("ExistingUserName")):
            raise MissingRequiredParametersException(" ExistingUserName  are/is requried")
        # return serilization type
        ret_type = args.get("RT")
        if ret_type is None:
            ret_type = "JSON"

        # current_node_envs = infa_env.get_envs(current_node.id)  # type: dict
        current_node_envs = get_current_node_infa_envs()
        os.environ.update(current_node_envs)
        mainLogger.debug("environment variables is {0}".format(current_node_envs))
        args.pop("RT")

        res = listUserPermissions(**args)
        mainLogger.debug(res)

        if ret_type.upper() == "PROTOBUF":
            proto_resp = infaCliResponse_pb2.InfaCliResponse()
            proto_resp.retcode = res.retcode
            proto_resp.stdout = str(res.stdout)
            res = proto_resp.SerializeToString()
            mainLogger.debug("protobuf: the result is {0}".format(res))
            content_type = Config.PREDEFINED_CONTENT_TYPES.get("PROTOBUF")
        else:
            output_dict = {"retcode": res.retcode,
                           "stdout": str(res.stdout)
                           }
            res = json.dumps(output_dict)
            content_type = Config.PREDEFINED_CONTENT_TYPES.get("JSON")
        response = make_response(res)
        response.headers["Content-Type"] = content_type
        return response


class ListUserPrivileges(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("ServiceName", type=str, help="Required")
        self.parser.add_argument("ExistingUserName", type=str, help="Required")
        self.parser.add_argument("ExistingUserSecurityDomain", type=str, default='Native',
                                 help="Optional, ExistingUserSecurityDomain")
        self.parser.add_argument("DomainName", type=str, default=None,
                                 help="Optional, Optional, if it's set the INFA_DEFAULT_DOMAIN")
        self.parser.add_argument("UserName", type=str, default=None,
                                 help="Optional, Optional, if it's set the INFA_DEFAULT_DOMAIN_USER")
        self.parser.add_argument("Password", type=str, default=None,
                                 help="Optional, Optional, if it's set the INFA_DEFAULT_DOMAIN_PASSWORD")
        self.parser.add_argument("SecurityDomain", type=str, default=None,
                                 help="Optional, Optional, if it's set the INFA_DEFAULT_SECURITY_DOMAIN")
        self.parser.add_argument("Gateway", type=str, default=None, help="Optional, Gateway")
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
        if is_none(args.get("ServiceName")) or is_none(args.get("ExistingUserName")):
            raise MissingRequiredParametersException(" ServiceName and  ExistingUserName  are/is requried")
        # return serilization type
        ret_type = args.get("RT")
        if ret_type is None:
            ret_type = "JSON"

        current_node_envs = get_current_node_infa_envs()
        os.environ.update(current_node_envs)
        mainLogger.debug("environment variables is {0}".format(current_node_envs))
        args.pop("RT")

        res = listUserPrivileges(**args)
        mainLogger.debug(res)

        if ret_type.upper() == "PROTOBUF":
            proto_resp = infaCliResponse_pb2.InfaCliResponse()
            proto_resp.retcode = res.retcode
            proto_resp.stdout = str(res.stdout)
            res = proto_resp.SerializeToString()
            mainLogger.debug("protobuf: the result is {0}".format(res))
            content_type = Config.PREDEFINED_CONTENT_TYPES.get("PROTOBUF")
        else:
            output_dict = {"retcode": res.retcode,
                           "stdout": str(res.stdout)
                           }
            res = json.dumps(output_dict)
            content_type = Config.PREDEFINED_CONTENT_TYPES.get("JSON")
        response = make_response(res)
        response.headers["Content-Type"] = content_type
        return response


class ListGroupsForUser(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("ExistingUserName", type=str, help="Required")
        self.parser.add_argument("ExistingUserSecurityDomain", type=str, default='Native',
                                 help="Optional, default is Native")
        self.parser.add_argument("DomainName", type=str, default=None,
                                 help="Optional, Optional, if it's set the INFA_DEFAULT_DOMAIN")
        self.parser.add_argument("UserName", type=str, default=None,
                                 help="Optional, Optional, if it's set the INFA_DEFAULT_DOMAIN_USER")
        self.parser.add_argument("Password", type=str, default=None,
                                 help="Optional, Optional, if it's set the INFA_DEFAULT_DOMAIN_PASSWORD")
        self.parser.add_argument("SecurityDomain", type=str, default=None,
                                 help="Optional, Optional, if it's set the INFA_DEFAULT_SECURITY_DOMAIN")
        self.parser.add_argument("Gateway", type=str, default=None, help="Optional, Gateway")
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
        if is_none(args.get("ExistingUserName")):
            raise MissingRequiredParametersException(" ExistingUserName  are/is requried")
        # return serilization type
        ret_type = args.get("RT")
        if ret_type is None:
            ret_type = "JSON"

        current_node_envs =get_current_node_infa_envs()
        os.environ.update(current_node_envs)
        mainLogger.debug("environment variables is {0}".format(current_node_envs))
        args.pop("RT")

        res = listGroupsForUser(**args)
        mainLogger.debug(res)

        if ret_type.upper() == "PROTOBUF":
            proto_resp = infaCliResponse_pb2.InfaCliResponse()
            proto_resp.retcode = res.retcode
            proto_resp.stdout = str(res.stdout)
            for group in res.stdout:
                groups_info_1 = proto_resp.messages.add()
                groups_info_1.value = group.get("groupName")
                groups_info_1.name = group.get("securityDomain")

            res = proto_resp.SerializeToString()
            mainLogger.debug("protobuf: the result is {0}".format(res))
            content_type = Config.PREDEFINED_CONTENT_TYPES.get("PROTOBUF")
        else:
            output_dict = {"retcode": res.retcode,
                           "stdout": str(res.stdout)
                           }
            res = json.dumps(output_dict)
            content_type = Config.PREDEFINED_CONTENT_TYPES.get("JSON")
        response = make_response(res)
        response.headers["Content-Type"] = content_type
        return response
