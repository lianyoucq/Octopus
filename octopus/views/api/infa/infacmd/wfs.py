# -*- coding:utf-8 -*-
import json
import os

from flask import make_response, g, Blueprint
from flask_restful import reqparse, Resource

from octopus.common import is_none
from octopus.common.logger import mainLogger
from octopus.database.metadata import get_current_node_infa_envs
from octopus.exceptions import MissingRequiredParametersException
from octopus.infa.infacmd.wfs import startWorkflow, listWorkflows, listTasks, listActiveWorkflowInstances, \
    listWorkflowParams
from octopus.views.api import infaCliResponse_pb2
from config import Config

infacmd_wfs_bp = Blueprint("wfs", __name__)


class StartWorkflow(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("DomainName", type=str, default=None,
                                 help="Optional, Optional, if it's set the INFA_DEFAULT_DOMAIN")
        self.parser.add_argument("ServiceName", type=str, help="Required")
        self.parser.add_argument("Application", type=str, help="Required")
        self.parser.add_argument("Workflow", type=str, help="Required")
        self.parser.add_argument("Wait", type=bool, default=False, help="Optional, Wait")
        self.parser.add_argument("ParameterFile", type=str, default=None, help="Optional, ParameterFile")
        self.parser.add_argument("ParameterSet", type=str, default=None, help="Optional, ParameterSet")
        self.parser.add_argument("UserName", type=str, default=None,
                                 help="Optional, Optional, if it's set the INFA_DEFAULT_DOMAIN_USER")
        self.parser.add_argument("Password", type=str, default=None,
                                 help="Optional, Optional, if it's set the INFA_DEFAULT_DOMAIN_PASSWORD")
        self.parser.add_argument("SecurityDomain", type=str, default=None,
                                 help="Optional, Optional, if it's set the INFA_DEFAULT_SECURITY_DOMAIN")
        self.parser.add_argument("ResilienceTimeout", type=str, default=None,
                                 help="Optional, Optional, if it's set the INFA_CLIENT_RESILIENCE_TIMEOUT")
        self.parser.add_argument("OsProfile", type=str, default=None, help="Optional, OsProfile")

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
        if is_none(args.get("ServiceName")) or is_none(args.get("Application")) or is_none(args.get("Workflow")):
            raise MissingRequiredParametersException(" ServiceName and  Application and  Workflow  are/is requried")
        # return serilization type
        ret_type = args.get("RT")
        if ret_type is None:
            ret_type = "JSON"

        # current_node_envs = infa_env.get_envs(current_node.id)  # type: dict
        current_node_envs = get_current_node_infa_envs()
        os.environ.update(current_node_envs)
        mainLogger.debug("environment variables is {0}".format(current_node_envs))
        args.pop("RT")

        res = startWorkflow(**args)
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


class ListWorkflows(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("DomainName", type=str, default=None,
                                 help="Optional, Optional, if it's set the INFA_DEFAULT_DOMAIN")
        self.parser.add_argument("ServiceName", type=str, help="Required")
        self.parser.add_argument("Application", type=str, help="Required")
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

        res = listWorkflows(**args)
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


class ListTasks(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("DomainName", type=str, default=None,
                                 help="Optional, Optional, if it's set the INFA_DEFAULT_DOMAIN")
        self.parser.add_argument("ServiceName", type=str, help="Required")
        self.parser.add_argument("UserName", type=str, default=None,
                                 help="Optional, Optional, if it's set the INFA_DEFAULT_DOMAIN_USER")
        self.parser.add_argument("Password", type=str, default=None,
                                 help="Optional, Optional, if it's set the INFA_DEFAULT_DOMAIN_PASSWORD")
        self.parser.add_argument("MaxTasks", type=int, default=None, help="Optional, MaxTasks")
        self.parser.add_argument("FilterByOwner", type=str, default=None, help="Optional, FilterByOwner")
        self.parser.add_argument("FilterByStatus", type=str, default=None, help="Optional, FilterByStatus")
        self.parser.add_argument("FilterByCreationDate", type=str, default=None, help="Optional, FilterByCreationDate")
        self.parser.add_argument("FilterByType", type=str, default=None, help="Optional, FilterByType")
        self.parser.add_argument("FilterByDueDate", type=str, default=None, help="Optional, FilterByDueDate")
        self.parser.add_argument("FilterByID", type=str, default=None, help="Optional, FilterByID")
        self.parser.add_argument("FilterByName", type=str, default=None, help="Optional, FilterByName")
        self.parser.add_argument("FilterByNameLike", type=str, default=None, help="Optional, FilterByNameLike")
        self.parser.add_argument("TasksOffset", type=str, default=None, help="Optional, TasksOffset")
        self.parser.add_argument("Role", type=str, default='ALL', help="Optional, Role")
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

        res = listTasks(**args)
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


class ListActiveWorkflowInstances(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("DomainName", type=str, default=None,
                                 help="Optional, Optional, if it's set the INFA_DEFAULT_DOMAIN")
        self.parser.add_argument("ServiceName", type=str, help="Required")
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

        res = listActiveWorkflowInstances(**args)
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


class ListWorkflowParams(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("ServiceName", type=str, help="Required")
        self.parser.add_argument("Application", type=str, help="Required")
        self.parser.add_argument("Workflow", type=str, help="Required")
        self.parser.add_argument("DomainName", type=str, default=None,
                                 help="Optional, Optional, if it's set the INFA_DEFAULT_DOMAIN")
        self.parser.add_argument("OutputFile", type=str, default=None, help="Optional, OutputFile")
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
        if is_none(args.get("ServiceName")) or is_none(args.get("Application")) or is_none(args.get("Workflow")):
            raise MissingRequiredParametersException(" ServiceName and  Application and  Workflow  are/is requried")
        # return serilization type
        ret_type = args.get("RT")
        if ret_type is None:
            ret_type = "JSON"

        current_node_envs = get_current_node_infa_envs()
        os.environ.update(current_node_envs)
        mainLogger.debug("environment variables is {0}".format(current_node_envs))
        args.pop("RT")

        res = listWorkflowParams(**args)
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
