# Octopus - RESTFUL API

## 管理API
### Inner Database - IDB
#### GET方法
GET方法显示API的使用方法或参数

#### POST 方法
初始化inner Database

#### DELETE 方法
删除inner Database数据

### Nodemeta XML API
#### GET 方法
GET方法显示API的使用方法或参数

#### POST 方法
解析nodemeta.xml文件，同时，加载数据到inner database

### Informatica 预定义环境变量 API
#### GET 方法
- 帮助
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

- 显示所有定义好的环境变量
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
- 显示指定的环境变量
```bash
curl http://localhost:5000/api/mgt/env/INFA_HOME,INFA_DEFAULT_DOMAIN -X GET
```
```json
{
    "INFA_HOME": "/opt/infa/pwc/1020",
    "INFA_DEFAULT_DOMAIN": "DM_ARTHUR_JELLYFISH"
}
```


#### POST 方法
- 创建一个环境变量到Inner Database里
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

- 创建多个环境变量到Inner Database里
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

- 更新一个已经存在的环境变量
```bash
curl http://localhost:5000/api/mgt/env -d "Envs=ICMD_JAVA_OPTS=-Xmx1024m" -X POST
```


#### PUT 方法
- 更新一个已经存在的环境变量
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

#### DELETE 方法
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

> 对于POST方法， 必须有参数名: Envs. 否则它将不会新建或者更新Informatica 环境变量
> 
> POST METHOD可以做更新操作, PUT在此API中也可以做插入操作，即POST/PUT操作是upsert操作。
> 请注意这点。


## Informatica API
> 注意:
> 
> 与标准的Restful API不同的是, 
> Informatica API使用GET方法来显示API的用法或参数，POST方法来调API

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
    
    - 指定备份路径
    
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
	"retcode": 0, 
 	"stdout": "blS+xC17ivblojrx4Hhsug=="
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
    stdout: [INFACMD_10052] Service [_adminconsole] Domain [DM_Arthur_Jellyfish] Host:Port [arthur-jellyfish.infaec.com:6005] was successfully pinged.
    messages: 
    ```

-  resetpassword
    > 错误信息示例
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

    这个函数比较费时
    
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



