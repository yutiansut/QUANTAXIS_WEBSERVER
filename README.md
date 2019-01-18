# QUANTAXIS_WEBSERVER
quantaxis_webserver


QUANTAXIS的持久化及后端解决方案

```
给了一个demo:  地址  www.yutiansut.com:8010
当前服务器部署版本: 1.3.4

```

## install
```
pip install https://github.com/yutiansut/tornado_http2/archive/master.zip

pip install quantaxis_webserver
```
## API


api参见: [backend_api](./backendapi.md)

## CHANGELOG
- 1.0 版本  基于原有quantaxisd的功能做移植

- 1.1 

    - 增加http2支持
    - [] 增加tls, ssl支持

    - 一个完备的websocket通讯/交易机制
    
- 1.3.3 
    - 增加windows服务(QUANTAXIS_Webservice)
    - 对应qadesktop 0.0.7 版本

- 1.3.4
    - 改用websocket+ json 的模式进行cs通信
    - 对应qadesktop 0.0.8 版本
    
- 1.3.5
    - 增加 USERHandler模型, 对应1.2.8+ 的quantaxis QA_USER
