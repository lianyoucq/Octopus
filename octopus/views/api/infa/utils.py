# -*- coding:utf-8 -*-
import os
from flask_restful import reqparse, Resource
from flask import Blueprint, abort, make_response, g
from octopus.infa.utils import pmpasswd
from octopus.database.metadata import get_current_node_infa_envs
from octopus.common.logger import mainLogger
import octopus.views.api.infaCliResponse_pb2 as infaCliResponse_pb2
import json
from config import Config

utils_bp = Blueprint("utils", __name__)
# utils_bp = Blueprint("utils", __name__)


class Pmpassword(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("Passwd",
                                 type=str,
                                 help='Password to be encrypted')
        self.parser.add_argument("EncryptType",
                                 type=str,
                                 default='CRYPT_SYSTEM',
                                 choices=['CRYPT_DATA', 'CRYPT_SYSTEM'],
                                 help="Encryption Type， CRYPT_DATA if it uses in the parameter file, otherwise, "
                                      "it's CRYPT_SYSTEM")
        self.parser.add_argument("RT",
                                 type=str,
                                 default='JSON',
                                 help="Return Type: (JSON|PROTOBUF)")

    def get(self):
        passwd_help_list = []
        for i in self.parser.args:
            passwd_parameters_dict = {}
            passwd_parameters_dict.update({"name": i.name, "help": i.help, "default": i.default})
            passwd_help_list.append(passwd_parameters_dict)
        return {"Usages": passwd_help_list}

    def post(self):
        args = self.parser.parse_args()
        mainLogger.info("the pmpasswd args is {0}".format(args))
        encrypt_type = args.get("EncryptType")
        passwd = args.get("Passwd")
        if encrypt_type is None or encrypt_type not in ('CRYPT_DATA', 'CRYPT_SYSTEM') or passwd is None:
            abort(401)
        ret_type = args.get('RT')  # type: str

        if ret_type is None:
            ret_type = "JSON"

        # node = Node()
        # current_node = node.get_current_node()  # type: Node
        #
        # infa_env = INFA_ENV()
        #
        # set_task_envs = infa_env.get_envs(current_node.id)
        set_task_envs = get_current_node_infa_envs()
        print("############## os.environ is {0}".format(os.environ))
        os.environ.update(set_task_envs)

        commandResult = pmpasswd(passwd, encrypt_type=encrypt_type)  # type: namedtuple("pmpasswdResult",
        #  ['retcode', 'stdout'])
        content_type = None
        if ret_type.upper() == "PROTOBUF":
            pmpasswd_resp = infaCliResponse_pb2.InfaCliResponse()
            pmpasswd_resp.retcode = commandResult.retcode
            pmpasswd_resp.stdout = commandResult.stdout
            commandResult = pmpasswd_resp.SerializeToString()
            mainLogger.debug("protobuf: the result is {0}".format(commandResult))
            content_type = Config.PREDEFINED_CONTENT_TYPES.get("PROTOBUF")
        else:
            commandResult = json.dumps(commandResult._asdict())
            content_type = Config.PREDEFINED_CONTENT_TYPES.get("JSON")
        response = make_response(commandResult)
        response.headers["Content-Type"] = content_type
        return response
