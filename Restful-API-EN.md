# Octopus - RESTFUL API

## Management API
### Inner Database - IDB
#### GET METHOD
It will show the API's usage

#### POST METHOD
It will init the inner database

#### DELETE METHOD
It will drop the inner database

### Nodemeta XML API
#### GET METHOD
It will show the API's usage

#### POST METHOD
It will parse the nodemeta.xml file and load into the inner database

### Informatica Environment variables API
#### GET METHOD
- help
```bash
 curl http://localhost:5000/api/mgt/env/help -X GET
```
```json
{
    "Usages": [
        {
            "name": "Envs",
            "help": "For GET method, it returns help if it's help; it returns all environment parameters if it's all;it returns specified environment parameters if it's env_name1,env_name2;For POST/PUT method, you can add multiple envs likes: env_name1=env_value1,env_name2=env_value2;For DELETE method,",
            "default": null
        }
    ]
}
```

- show all defined environment variables
```bash
curl http://localhost:5000/api/mgt/env/all -X GET
```
```json
{
    "INFA_DEFAULT_USER_PASSWORD": "FKoR99HKUmkp1bNTAILqkA==",
    "INFA_DEFAULT_DOMAIN_USER": "admin",
    "INFA_HOME": "/opt/infa/pwc/1020",
    "INFA_DEFAULT_DOMAIN": "DM_ARTHUR_JELLYFISH"
}
```
- show specified environment variables
```bash
curl http://localhost:5000/api/mgt/env/INFA_HOME,INFA_DEFAULT_DOMAIN -X GET
```
```json
{
    "INFA_HOME": "/opt/infa/pwc/1020",
    "INFA_DEFAULT_DOMAIN": "DM_ARTHUR_JELLYFISH"
}
```


#### POST METHOD
- Create a Informatica environment variable
```bash
curl http://localhost:5000/api/mgt/env -d "Envs=ICMD_JAVA_OPTS=-Xmx1024m" -X POST
```
```json
{
    "retcode": 0,
    "stdout": {
        "ICMD_JAVA_OPTS": "-Xmx1024m"
    },
    "stderr": null
}
```

- Create multiple Informatica environment variables
```bash
curl http://localhost:5000/api/mgt/env -d "Envs=INFA_DEFAULT_DATABASE_PASSWORD=0OY4DwDzkHzptF0dg8ErXQ==,INFA_DEFAULT_SECURITY_DOMAIN=Native" -X POST
```
```json
{
    "retcode": 0,
    "stdout": {
        "INFA_DEFAULT_DATABASE_PASSWORD": "0OY4DwDzkHzptF0dg8ErXQ==",
        "INFA_DEFAULT_SECURITY_DOMAIN": "Native"
    },
    "stderr": null
}
```

- update the existing Informatica environment variables
```bash
curl http://localhost:5000/api/mgt/env -d "Envs=ICMD_JAVA_OPTS=-Xmx1024m" -X POST
```


#### PUT METHOD
- update the existing Informatica environment variables
```bash
curl http://localhost:5000/api/mgt/env/ICMD_JAVA_OPTS=-Xmx2048m -X PUT
```
```json
{
    "retcode": 0,
    "stdout": {
        "ICMD_JAVA_OPTS": "-Xmx2048m"
    },
    "stderr": null
}
```

#### DELETE METHOD
```bash
curl http://localhost:5000/api/mgt/env/ICMD_JAVA_OPTS -X DELETE
```
```json
{
    "retcode": 0,
    "stdout": "ICMD_JAVA_OPTS",
    "stderr": ""
}

```

> For POST METHOD, it must have the parameter name: Envs,
> otherwise, it won't create or update Informatica Environment variables
>
> The POST METHOD can update existing environment variables, The PUT METHOD will create environment variables, 
> So POST/PUT method are upsert operations. 
> Please pay attention on this.



## Informatica API
> Warning:
> 
> Unlike the classic Restful API, 
> the Informatica API here is a little different, the GET METHOD shows the usage, while the POST METHOD execute the API

### infasetup
-  backupdomain
    ```bash
   curl http://127.0.0.1:5000/api/infasetup/backupdomain -X GET
    ```
    ```json
    {
        "Usages": [
            {
                "name": "backup_path",
                "help": "backup path, default is workdir/<Domain_Name>/",
                "default": "/home/arthur/python/octopus/workdir"
            },
            {
                "name": "RT",
                "help": "Return Type(JSON|PROTOBUF)",
                "default": "JSON"
            }
        ]
    }
   ```
    
    - specify the backup_path
    
    ```bash
    curl -d 'backup_path=/tmp' http://127.0.0.1:5000/api/infa/infasetup/backupdomain -X POST -v
    ```

### utils
-  pmpasswd

    -  json
    
    ```bash
    curl -d 'Passwd=infa' http://127.0.0.1:5000/api/infa/utils/pmpasswd -X POST -v
    ```
    
    ```json
    {
        "status": "Success",
        "retCode": 0,
        "message": "TWuNzDbE2H9XA7BPmCgxrg=="
    }
    ```

    - protobuf
    
      ```bash
        curl -d 'Passwd=infa&RT=protobuf' http://127.0.0.1:5000/api/infa/utils/pmpasswd -X POST -v > passwd.dat
        
        python parse_protobuf.py passwd.dat
        retcode: 0
        stdout: 3WhkU+IUREF2mPsuWWRFuA==
        messages:
      ```

### infacmd - isp
-  ping

    ```bash
    curl -d 'ServiceName=_adminconsole&RT=protobuf' http://0.0.0.0:5000/api/infa/infacmd/isp/ping -X POST -v > ping.dat
    
    python parse_protobuf.py ping.dat
    retcode: 0
    stdout: [INFACMD_10052] Service [_adminconsole] Domain [DM102_INFA210] Host:Port [infa210.sleety.com:6408] was successfully pinged.
    messages: 
    ```

-  resetpassword
    > Error message
    ```bash
    curl http://localhost:5000/api/infa/infacmd/isp/resetpassword -X POST   
    Error: 'The ServiceName and ResetUserPassword are required, not the None and None'%
    ```

-  purgelog

    ```bash
    curl localhost:5000/api/infa/infacmd/isp/purgelog -X POST
    ```
    
    ```json
    {
        "retcode": 0,
        "stdout": "Command ran successfully.\n"
    }
    ```

-  enableserviceprocess 

    It will last long time
    
    ```bash
    curl -d "ServiceName=IS_ASCII&NodeName=ND_INFA210" localhost:5000/api/infa/infacmd/isp/enableserviceprocess -X POST
    ```
    
    ```json
    {
        "retcode": 255,
        "stdout": "[ICMD_10033] Command [EnableServiceProcess] failed with error [[INFACMD_40000] [DOM_10139] Cannot enable the service process for service [IS_ASCII] on node [ND_INFA210] because it is already enabled or is in the process of being shut down. Verify that the service process is shut down before you enable it.].\n"
    }
    ```
    
-  enableservice

    ```bash
    curl -d "ServiceName=IS_ASCII" localhost:5000/api/infa/infacmd/isp/enableservice -X POST
    ```
    
    ```json
    {
        "retcode": 255, 
        "stdout": "[ICMD_10033] Command [EnableService] failed with error [[INFACMD_40000] [DOM_10071] Request to enable service [IS_ASCII] failed because it is already enabled.].\n"}
    ```

-  disableserviceprocess

    ```bash
    curl -d "ServiceName=IS_ASCII&NodeName=ND_INFA210&Mode=Abort" localhost:5000/api/infa/infacmd/isp/disableserviceprocess -X POST
    ```


-  disableservice

    ```bash
    curl -d "ServiceName=IS_ASCII&Mode=Abort" localhost:5000/api/infa/infacmd/isp/disableservice -X POST
    ```

-  listgroupsforuser

    ```bash
    curl -d "ExistingUserName=admin" http://localhost:5000/api/infa/infacmd/isp/listgroupsforuser -X POST
    ```
    ```json
    {
        "retcode": 0,
        "stdout": "[{'securityDomain': 'Native', 'groupName': 'Administrator'}, {'securityDomain': 'Native', 'groupName': 'Everyone'}]"
    }
    ```

-  listnoderesources
-  listnodes

-  listservicelevels
-  listservices

-  listservicenodes
-  listserviceprivileges
-  getservicestatus
-  listlicenses
-  showlicense
-  listallusers
-  listconnections,
-  listconnectionoptions
-  listuserpermissions
-  listuserprivileges

### infacmd - dis

-  listapplications
-  listapplicationobjects
-  stopblazeservice
-  backupapplication
-  stopapplication
-  startapplication

### infacmd - mrs

- backupcontents

### infacmd - ms

- listmappings
- runmapping
- getmappingstatus
- getrequestlog
- listmappingparams

### infacmd - oie

- deployapplication

### infacmd - wfs

- startworkflow
- listworkflows
- listtasks
- listactiveworkflowinstances
- listworkflowparams



