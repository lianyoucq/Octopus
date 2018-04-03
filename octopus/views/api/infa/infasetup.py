# -*- coding:utf-8 -*-
import json
import os

from flask import Blueprint, make_response, g
from flask_restful import reqparse, Resource

from octopus.common.logger import mainLogger
from octopus.common.path_utils import get_backup_dir

from octopus.exceptions import UnsupportedOperationsException
from octopus.infa.infasetup import backupDomain
from octopus.views.api import infaCliResponse_pb2
from config import Config

infasetup_bp = Blueprint("infasetup", __name__)


class Backup_domain(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("backup_path",
                                 type=str,
                                 default=get_backup_dir(),
                                 help='backup path, default is workdir/<Domain_Name>/')
        self.parser.add_argument("RT",
                                 type=str,
                                 default="JSON",
                                 help="Return Type(JSON|PROTOBUF)")

    def get(self):
        backup_domain_help_list = []
        for i in self.parser.args:
            backup_domain_parameters_dict = {}
            backup_domain_parameters_dict.update({"name": i.name, "help": i.help, "default": i.default})
            backup_domain_help_list.append(backup_domain_parameters_dict)
        return {"Usages": backup_domain_help_list}

    def post(self):
        """
        提交backup domain命令
        :return:
        """
        args = self.parser.parse_args()
        mainLogger.info(args)
        backup_path = args.get('backup_path')

        # return serilization type
        ret_type = args.get('RT')  # type: str
        if ret_type is None:
            ret_type = "JSON"

        # domain = Domain()
        current_domain = g.domain  # type: agent.database.metadata.Domain

        # node = Node()
        # current_node = node.get_current_node()  # type: Node
        current_node = g.current_node # type: agent.database.metadata.Node


        if not current_node.is_gateway:
            raise UnsupportedOperationsException(
                "current node is worker node, it doesn't supported to backup domain operation")

        # infa_env = INFA_ENV()
        # current_node_envs = infa_env.get_envs(current_node.id)  # type: dict
        current_node_envs = g.infa_envs # type: dict
        os.environ.update(current_node_envs)
        mainLogger.debug("environment variables is {0}".format(current_node_envs))
        commandResult = backupDomain(domainname=current_domain.name,
                                     databasetype=current_domain.db_type,
                                     databaseaddress="{0}:{1}".format(current_domain.db_host.rstrip(),
                                                                       current_domain.db_port),
                                     databaseusername=current_domain.db_username,
                                     databaseservicename=current_domain.db_service_name,
                                     backupfile=backup_path,
                                     force=False,
                                     tablespace=current_domain.db_tablespace,
                                     schemaname=current_domain.db_schema,
                                     databasetlsenabled=current_domain.db_tls_enabled,
                                     databasetruststorepassword=current_domain.db_truststorepassword,
                                     trustedconnection=current_domain.db_trustedconnection,
                                     encryptionkeylocation=current_node.sc_secretkeysdirectory,
                                     databasetruststorelocation=current_domain.db_truststore_location
                                     )
        message = "backupfile: {0}".format(commandResult.backupfile)
        output_dict = {"retcode": commandResult.retcode,
                       "stdout": commandResult.stdout,
                       "messages": message}
        mainLogger.info(output_dict)

        if ret_type.upper() == "PROTOBUF":
            backdomain_resp = infaCliResponse_pb2.InfaCliResponse()
            backdomain_resp.retcode = commandResult.retcode
            backdomain_resp.stdout = commandResult.stdout
            backup_info = backdomain_resp.messages.add()
            backup_info.name = "backupfile"
            backup_info.value = commandResult.backupfile
            commandResult = backdomain_resp.SerializeToString()
            mainLogger.debug("protobuf: the result is {0}".format(commandResult))
            content_type = Config.PREDEFINED_CONTENT_TYPES.get("PROTOBUF")
        else:
            commandResult = json.dumps(output_dict)
            content_type = Config.PREDEFINED_CONTENT_TYPES.get("JSON")
        response = make_response(commandResult)
        response.headers["Content-Type"] = content_type
        return response

# ##################################################
