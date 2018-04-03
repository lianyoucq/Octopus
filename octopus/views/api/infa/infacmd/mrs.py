# -*- coding:utf-8 -*-
import json
import os

from flask import Blueprint, make_response, g
from flask_restful import reqparse, Resource

from octopus.common import is_none
from octopus.common.logger import mainLogger
from octopus.database.metadata import get_current_node_infa_envs
from octopus.exceptions import MissingRequiredParametersException
from octopus.infa.infacmd.mrs import backupContents
from config import Config
from octopus.views.api import infaCliResponse_pb2


infacmd_mrs_bp = Blueprint("mrs", __name__)


class BackupContents(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("ServiceName", type=str, help="Required")
        self.parser.add_argument("OutputFileName", type=str, help="Required")
        self.parser.add_argument("DomainName", type=str, default=None,
                                 help="Optional, Optional, if it's set the INFA_DEFAULT_DOMAIN")
        self.parser.add_argument("SecurityDomain", type=str, default=None,
                                 help="Optional, Optional, if it's set the INFA_DEFAULT_SECURITY_DOMAIN")
        self.parser.add_argument("UserName", type=str, default=None,
                                 help="Optional, Optional, if it's set the INFA_DEFAULT_DOMAIN_USER")
        self.parser.add_argument("Password", type=str, default=None,
                                 help="Optional, Optional, if it's set the INFA_DEFAULT_DOMAIN_PASSWORD")
        self.parser.add_argument("OverwriteFile", type=False, default=None, help="Optional, OverwriteFile")
        self.parser.add_argument("Description", type=str, default=None, help="Optional, Description")
        self.parser.add_argument("BackupSearchIndices", type=str, default=None, help="Optional, BackupSearchIndices")
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
        if is_none(args.get("ServiceName")) or is_none(args.get("OutputFileName")):
            raise MissingRequiredParametersException(" ServiceName and  OutputFileName  are/is requried")
        # return serilization type
        ret_type = args.get("RT")
        if ret_type is None:
            ret_type = "JSON"

        # current_node_envs = infa_env.get_envs(current_node.id)  # type: dict
        current_node_envs = get_current_node_infa_envs()
        os.environ.update(current_node_envs)
        mainLogger.debug("environment variables is {0}".format(current_node_envs))
        args.pop("RT")

        res = backupContents(**args)
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