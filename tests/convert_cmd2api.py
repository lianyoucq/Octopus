# -*- coding:utf-8 -*-
import inspect

PREDEFINED_PARAMETERS = {'DomainName': "Optional, if it's set the INFA_DEFAULT_DOMAIN",
                         'UserName': "Optional, if it's set the INFA_DEFAULT_DOMAIN_USER",
                         'Password': "Optional, if it's set the INFA_DEFAULT_DOMAIN_PASSWORD",
                         'SecurityDomain': "Optional, if it's set the INFA_DEFAULT_SECURITY_DOMAIN",
                         'ResilienceTimeout': "Optional, if it's set the INFA_CLIENT_RESILIENCE_TIMEOUT", }


def get_cmd_parameters(func):
    sigs = inspect.signature(func)
    parameters = sigs.parameters

    my_parameters = ""
    required_parameters = list()

    for pn, pv in parameters.items():  # type: str, str
        pv = str(pv)
        if pn in PREDEFINED_PARAMETERS.keys():
            my_parameters += "        self.parser.add_argument(\"{0}\", type=str, default=None, help=\"Optional, {1}\")\n".format(
                pn,
                PREDEFINED_PARAMETERS.get(pn))
        elif pv and pv.__contains__("="):
            pn_type = pv[pv.index(":") + 1:pv.index("=")]
            if not pn_type:
                pn_type = "int"
            pn_default = pv[pv.index("=") + 1:]

            my_parameters += "        self.parser.add_argument(\"{0}\", type={1}, default={2}, help=\"Optional, {3}\")\n".format(
                pn,
                pn_type,
                pn_default, pn)
        elif pv and pv.__contains__(":"):
            pn_type = pv[pv.index(":") + 1:]
            my_parameters += "        self.parser.add_argument(\"{0}\", type={1}, help=\"Required\")\n".format(pn,
                                                                                                               pn_type,
                                                                                                               pn
                                                                                                               )
            required_parameters.append(pn)
        else:
            my_parameters += "        self.parser.add_argument(\"{0}\", type=str, help=\"Required, {1}\")\n".format(pn,
                                                                                                                    pn
                                                                                                                    )
            required_parameters.append(pn)

    return (my_parameters, required_parameters)


isp_commands = ["listServiceLevels", "listServices", "listServiceNodes", "listServicePrivileges", "getServiceStatus",
                "listLicenses", "showLicense", "listAllUsers", "listConnections", "listConnectionOptions",
                "listUserPermissions", "listUserPrivileges", "listGroupsForUser", ]

dis_commands = ["listApplications", "listApplicationObjects", "stopBlazeService", "backupApplication",
                "stopApplication", "startApplication", ]

mrs_commands = ['backupContents']

ms_commands = ["listMappings", "runMapping", "getMappingStatus", "getRequestLog", "listMappingParams", ]

oie_commands = ['deployApplication']

wfs_commands = ["startWorkflow", "listWorkflows", "listTasks", "listActiveWorkflowInstances", "listWorkflowParams", ]

commands = wfs_commands

# import octopus.infa.infacmd.isp as model
import octopus.infa.infacmd.wfs as model

for cmd in commands:
    if hasattr(model, cmd):
        inst = getattr(model, cmd)
        # if is_none(args.get("NodeName")):
        #     raise MissingRequiredParametersException("The NodeName is required")

        parameters, required_parameter_list = get_cmd_parameters(inst)
        required_parameters = " if "
        required_parameters_exceptions = "    raise MissingRequiredParametersException(\""
        for param in required_parameter_list:
            required_parameters += " is_none(args.get(\"{0}\")) or ".format(param)
            required_parameters_exceptions += " {0} and ".format(param)
        required_parameters_exceptions = required_parameters_exceptions[:-4] + " are/is requried\")"
        required_parameters = required_parameters[:-3] + ":"

        class_name = cmd[0:1].upper() + cmd[1:]
        clsdefinition = """
class """ + class_name + """(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()\n""" + parameters + """
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
       """ + required_parameters + "\n          " + required_parameters_exceptions + """
        # return serilization type
        ret_type = args.get("RT")
        if ret_type is None:
            ret_type = "JSON"

        # current_node_envs = infa_env.get_envs(current_node.id)  # type: dict
        current_node_envs = g.infa_envs
        os.environ.update(current_node_envs)
        mainLogger.debug("environment variables is {0}".format(current_node_envs))
        args.pop("RT")

        res = """ + cmd + """(**args)
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
"""

        print(clsdefinition)
        print("\n")
