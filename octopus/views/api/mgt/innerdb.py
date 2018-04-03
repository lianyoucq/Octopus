# -*- coding:utf-8 -*-
from flask import Blueprint
from flask_restful import reqparse, Resource

from octopus.common import is_none
from octopus.common.logger import mainLogger
from octopus.database import db
from octopus.database.metadata import INFA_ENV, get_current_node
from octopus.exceptions import WrongEnvrionmentFormatException
from octopus.utils.loadNodeMeta import load_metadata

mgt_idb_bp = Blueprint("innerdb", __name__)


class IDB(Resource):
    def __init__(self):
        pass

    def get(self):
        return {"Usages": "For POST method, Init the Inner Database; For DELETE method, Drop the Inner Database"}

    def post(self):
        output = {"retcode": 0, "stdout": "success"}
        try:
            db.create_all(bind="octopus_inner")
        except Exception as e:
            mainLogger.exception(str(e))
            output = {"retcode": 1, "stdout": str(e.args)}

        return output

    def delete(self):
        output = {"retcode": 0, "stdout": "success"}
        try:
            db.drop_all(bind="octopus_inner")
        except Exception as e:
            mainLogger.exception(str(e))
            output = {"retcode": 1, "stdout": str(e.args)}
        return output


class NodeMetaXML(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("Nodemeta_XML",
                                 type=str,
                                 help='nodemeta.xml file')

    def get(self):
        passwd_help_list = []
        for i in self.parser.args:
            passwd_parameters_dict = {}
            passwd_parameters_dict.update({"name": i.name, "help": i.help, "default": i.default})
            passwd_help_list.append(passwd_parameters_dict)
        return {"Usages": passwd_help_list}

    def post(self):
        args = self.parser.parse_args()
        mainLogger.info("the Nodemeta_XML args is {0}".format(args))

        nodemeta_xml_file = args.get("Nodemeta_XML")

        output = {"retcode": 0, "stdout": "success"}
        try:
            load_metadata(nodemeta_xml_file=nodemeta_xml_file)
        except Exception as e:
            mainLogger.exception(str(e))
            messages = str(e.args)
            output = {"retcode": 1, "stdout": messages}
        return output


class InfaEnvs(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("Envs",
                                 type=str,
                                 default=None,
                                 help="For GET method, it returns help if it's help; "
                                      "it returns all environment parameters if it's all;"
                                      "it returns specified environment parameters if it's env_name1,env_name2;"
                                      "For POST/PUT method, you can add multiple envs likes:"
                                      " env_name1=env_value1,env_name2=env_value2;"
                                      "For DELETE method,")

    def get(self, envs: str = "help"):
        current_node = get_current_node()
        infa_env_inst = INFA_ENV()
        if envs.lower() == "help":
            passwd_help_list = []
            for i in self.parser.args:
                passwd_parameters_dict = {}
                passwd_parameters_dict.update({"name": i.name, "help": i.help, "default": i.default})
                passwd_help_list.append(passwd_parameters_dict)
            return {"Usages": passwd_help_list}
        elif envs.lower() == "all":
            infa_envs_dict = infa_env_inst.get_envs(current_node.id)
            return infa_envs_dict
        else:
            infa_envs_dict = dict()
            envs_list = envs.split(",")
            for env in envs_list:
                env_dict = infa_env_inst.get_env(current_node.id, env)
                for key, value in env_dict.items():  # loop 1 time
                    infa_envs_dict.setdefault(key, value)
            return infa_envs_dict

    def post(self):
        args = self.parser.parse_args()

        mainLogger.debug("the AddInfaEnvs args is {0}".format(args))
        mainLogger.debug("the AddInfaEnvs locals is {0}".format(locals()))
        infa_envs_args = args.get("Envs")  # type: str
        infa_envs_dict = dict()

        try:
            envs_list = infa_envs_args.split(",")
            for env in envs_list:
                env_list = env.split("=", maxsplit=1)
                if len(env_list) < 2:
                    raise WrongEnvrionmentFormatException(
                        "{0} is not right, the standard format is env_name=env_value".format(env))
                infa_envs_dict.setdefault(env_list[0], env_list[1])
            current_node = get_current_node()
            infa_env_inst = INFA_ENV()
            ## upsert
            for key, value in infa_envs_dict.items():
                env_dict = {key: value}
                try:
                    infa_env_inst.update_env(current_node.id, env_dict)
                except Exception as e:
                    mainLogger.exception(
                        "Updating {0} with error: {1}, and now try to insert it".format(env_dict, str(e)))
                    infa_env_inst.insert_env(current_node.id, env_dict)
            ret_message = {"retcode": 0, "stdout": infa_envs_dict,
                           "stderr": None}
        except Exception as e:
            mainLogger.exception(str(e))

            ret_message =({"retcode": 1, "stdout": None,
                           "stderr": "Error {0} when upserting {1} into inner database.".format(str(e.args),
                                                                                                infa_envs_dict)}, 404)
        return ret_message

    def put(self, envs: str):
        self.parser.add_argument("Envs", default=envs )
        output = self.post()
        return output

    def delete(self, envs: str):
        mainLogger.debug("InfaEnvs Delete method  parameters is {0}".format(envs))
        current_node = get_current_node()
        infa_env_inst = INFA_ENV()
        envs_list = envs.split(",")
        stdout = ""
        stderr = ""
        for env in envs_list:
            try:
                infa_env_inst.delele_env(current_node.id, env=env)
                stdout += "{0}, ".format(env)
            except Exception as e:
                mainLogger.exception(str(e))
                stderr += "Delete the {0} with error {1} or it's not exisitng. \t".format(env, str(e.args))

        ret_message = {"retcode": 0, "stdout": stdout[:-2], "stderr": stderr}

        return ret_message

