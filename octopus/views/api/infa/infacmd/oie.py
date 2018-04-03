# -*- coding:utf-8 -*-
import json
import os

from flask import make_response, g, Blueprint
from flask_restful import reqparse, Resource

from octopus.common import is_none
from octopus.common.logger import mainLogger
from octopus.database.metadata import get_current_node_infa_envs
from octopus.exceptions import MissingRequiredParametersException
from octopus.infa.infacmd.oie import deployApplication
from octopus.views.api import infaCliResponse_pb2
from config import Config

infacmd_oie_bp = Blueprint("oie", __name__)


class DeployApplication(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("RepositoryService", type=str, help="Required")
        self.parser.add_argument("OutputDirectory", type=str, help="Required")
        self.parser.add_argument("ApplicationPath", type=str, help="Required")
        self.parser.add_argument("DomainName", type=str, default=None,
                                 help="Optional, Optional, if it's set the INFA_DEFAULT_DOMAIN")
        self.parser.add_argument("UserName", type=str, default=None,
                                 help="Optional, Optional, if it's set the INFA_DEFAULT_DOMAIN_USER")
        self.parser.add_argument("Password", type=str, default=None,
                                 help="Optional, Optional, if it's set the INFA_DEFAULT_DOMAIN_PASSWORD")

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
        if is_none(args.get("RepositoryService")) or is_none(args.get("OutputDirectory")) or is_none(
                args.get("ApplicationPath")):
            raise MissingRequiredParametersException(
                " RepositoryService and  OutputDirectory and  ApplicationPath  are/is requried")
        # return serilization type
        ret_type = args.get("RT")
        if ret_type is None:
            ret_type = "JSON"

        # current_node_envs = infa_env.get_envs(current_node.id)  # type: dict
        current_node_envs = get_current_node_infa_envs()
        os.environ.update(current_node_envs)
        mainLogger.debug("environment variables is {0}".format(current_node_envs))
        args.pop("RT")

        res = deployApplication(**args)
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
