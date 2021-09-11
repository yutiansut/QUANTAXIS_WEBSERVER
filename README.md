# QUANTAXIS_WEBSERVER
quantaxis_webserver


QUANTAXIS的后端基类 BASE ON TORNADO

```
current version: 2.0


2.0 支持了 tornado 6.1, 方便兼容 jupyterlab 3

2.0是一个不兼容更新, 删除了 1.x 的诸多 handlers, 如需使用之前的版本, 请指定版本安装 pip install quantaxis_webserver<2
```


-- support tornado 6.1


-- 支持 apschedule



选择直接 [use template](https://github.com/yutiansut/QUANTAXIS_WEBSERVER/generate) 创建 fork

自行修改你的 schedule


### COMPONENTS


- QAWebServer.basehandlers.QABaseHandler 
    - 支持 get/ post 的复写


    ```python
    
    class xxx(QABaseHander):
        def get(self):
            pass

        def post(self):
            pass
    ```

- QAWebServer.basehandlers.QAWebSocketHandler websocket 基类


- QAWebServer.schdeulehandler.QASchedulerHandler 定时任务基类


    - 本项目使用 TornadoScheduler, 基于 mongodb存储 job 信息
    - 使用 qaenv 获取 mongodb_ip, mongodb_port 如需修改地址
        - 使用 docker-compose 预制在系统变量中
        - 如未使用 docker-compose 自行修改系统环境变量
            - MONGODB ==> ip 默认 "127.0.0.1"
            - MONGODBPORT ==> port 默认 27017



    在初始化 init_scheduler 后, scheduler(Tornado Scheduler)是一个全局变量 可以直接使用(已经初始化在 start_server 函数中)

    复写QASchedulerHandler, 并放置到 handlers 句柄中

