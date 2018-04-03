[English](README.md) | [中文](README_CN.md)
# Octopus  - 章鱼

可以在Informatica Platform一台机器上运行，
也可以在其他没有安装Informatica Platform的机器上运行，不过此时需要安装Informatica Command Utilites（ICU）, ICU可以在Informatica介质下载页面下载

## Python 
版本: 3.x

# 依赖
[requirements.txt](requirements.txt)

## Python API
[Python API](Python-API.md)

## Restful API 帮助文档
[Restful API](Restful-API-CN.md)


## SSL
你可以参考下面的命令产生public和private cert文件
```bash
  openssl req -x509 -newkey rsa:4096 -nodes -out publiccert.pem -keyout privatekey.pem -days 365
```

## 作者
| 姓名        | Email           | Wechat  | Wechat订阅号  |
| :-------------: |:-------------:| :-----: | :------: |
| Arthur Li (李联友)    | 845201629@qq.com | Matchstick_men_v | INFAer |
