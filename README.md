# Scrapycw

## 概述
Scrapycw是一个Scrapy监控程序，你可以通过命令行或者web服务的方式监控Scrapy爬虫运行情况，以及进行运行爬虫等常用操作。

## 依赖

- Python 3.5+
- 操作系统：Linux, Mac OSX

## 安装

在项目根目录下克隆项目 scrapycw
```
$ git clone git@github.com:erygreat/scrapycw.git
```

<font color="red">暂不支持通过pip安装（不久之后会支持,）</font>

安装依赖包
```
$ pip3 install -r scrapycw/requirements.txt
```

初始化项目，创建数据库(安装后或版本升级都需要运行该命令)
```
python3 scrapycw/main.py init
```

## 使用方式

### 1. 命令行
可以使用 scrapycw 下的main.py脚本在控制台下运行命令

可用命令：

- init
- projectlist
- spiderlist
- server
- crawl
- stop

#### init命令
语法：`python3 scrapycw/main.py init`

说明：初始化项目，创建数据库表结构，安装或版本升级后都需要运行该命令（后续会使用其他方式自动执行），目前仅支持sqlite3，数据库文件在`RUNTIME_PATH`下

示例：
```
$ python3 scrapycw/main.py init

=========== 开始初始化 ===========
==== 创建数据库表 ===
Operations to perform:
  Apply all migrations: api
Running migrations:
  No migrations to apply.
=========== 初始化完成 ===========
```

#### crawl命令

语法: `python3 scrapycw/main.py crawl <spider-name> [-p <project>] [-a <爬虫参数>] [-s <scrapy设置]`

说明: 启动爬虫

示例：
```
$ python3 scrapycw/main.py crawl ipip -p dmhy
{'job_id': '20200129_131016_pouL0B', 'project': 'dmhy', 'spider': 'ipip', 'log_file': '/Users/mac/Git/spider/logs/scrapy.spiders.ipip_spider_2020_1_29.log', 'telnet': {'host': '127.0.0.1', 'port': 6024, 'username': 'scrapy', 'password': 'a78971039f8a176a'}}

$ python3 scrapycw/main.py crawl ipip -p dmhy -a name=zhangsan
{"job_id": "20200129_170543_y74To1", "project": "dmhy", "spider": "ipip", "log_file": "/Users/mac/Git/spider/logs/scrapy_dmhy.spiders.ipip_spider_2020_1_29.log", "telnet": {"host": "127.0.0.1", "port": 6023, "username": "scrapy", "password": "85b242b121624500"}}

$ python3 scrapycw/main.py crawl ip
{"success": false, "message": "Spider not found: ip", "project": "default", "spider": "ip"}
```

#### stop命令

语法: `python3 scrapycw/main.py stop <job-id>`

说明: 关闭爬虫

示例：
```
$ python3 scrapycw/main.py stop 20200129_131016_pouL0B
{"success": true, "project": "dmhy", "spider": "ipip", "message": "Finish", "status": "pending"}

$ python3 scrapycw/main.py stop 20200129_131016_pouL0B
{"success": false, "project": "dmhy", "spider": "ipip", "message": "Spider is Closed: timed out", "status": "close"}

$ python3 scrapycw/main.py stop 20200129_131016_pouL0B
{"success": false, "project": "dmhy", "spider": "ipip", "message": "Spider is Closed: [Errno 61] Connection refused", "status": "close"}
```

响应结果：

- status: 爬虫状态, pending表示正在关闭, close 表示已经关闭（可能telnet还未关闭，但是此时爬虫已经停止了）
- message: 操作消息，Finish表示完成，其他的表示爬虫已关闭

#### projectlist命令
语法：`python3 scrapycw/main.py projectlist`

说明：获取当前工作目录下所有的scrapy项目名称

示例：

```
$ python3 scrapycw/main.py projectlist
{"success": true, "message": null, "projects": [{"name": "default"}, {"name": "dmhy"}]}
```

#### spiderlist命令
语法：`python3 scrapycw/main.py spiderlist [-p <project>]`

说明：获取当前工作目录下某个scrapy项目下面所有爬虫的名称

属性：

- -p: scrapy项目名称，默认值为default

示例：

```
$ python3 scrapycw/main.py spiderlist -p dmhy
{"success": true, "message": null, "spiders": [{"name": "ipip"}], "project": "dmhy"}
```

#### server命令
语法：`python3 scrapycw/main.py server [<sub-command>] [--port <端口>] [--host <允许访问的地址>]`

说明：启动一个web服务，可以通过http请求获取scrapy服务信息

子命令:

- start: 开启web服务（默认值）
- stop: 关闭web服务
- restart: 重启web服务

属性：

start/restart命令：

- --port：web服务端口，默认值为2312，可以通过覆盖 SERVER_PORT 修改默认值
- --host：web服务允许访问地址，默认值为localhost，如果设置为 0 表示完全开放，允许所有IP访问，可以通过覆盖 SERVER_HOST 修改默认值
- --daemon：后台启动web服务（开启一个守护进程）

示例：
```bash
$ # 开启一个web服务
$ python3 scrapycw/main.py server start --port 8080 --host 0 --daemon
start web service ...

$ python3 scrapycw/main.py server stop
stop web server...
关闭进程成功! 进程ID: 19572
关闭进程成功! 进程ID: 19581
关闭web service 完成

$ python3 scrapycw/main.py server restart --daemon
stop web server...
关闭进程成功! 进程ID: 19976
关闭进程成功! 进程ID: 19985
关闭web service 完成

start web service ...
```

### 2. web接口
使用`server`命令启动一个web服务，然后就可以通过web接口方式控制scray运行。见![server](#### server命令)
#### 获取项目列表

- 请求地址：`/api/project-list`
- 请求方式：Get
- 请求参数：无
- 响应结果：
```
{
    "success": true,
    "message": null,
    "projects": [
        {
            "name": "default"
        },
        {
            "name": "play"
        }
    ]
}
```
- 示例：
```
$ curl "localhost:3984/api/project-list"
{"status": "success", "message": null, "projects": [{"name": "default"}, {"name": "play"}]}
```

#### 获取爬虫列表

- 请求地址：`/api/spider-list`
- 请求方式：Get
- 请求参数：

|请求参数|类型|是否允许为空|默认值|示例|
|---|---|---|---|---|
|project| string | 是 | default| default|

- 响应结果：
```
{
    "success": true,
    "spiders": [
        {
            "name": "ipip"
        },
        {
            "name": "daili"
        }
    ],
    "project": "dmhy"
}
```
- 示例：
```
$ curl "localhost:3984/api/spider-list"
{"success": true, "message": null, "spiders": [{"name": "baiduyun_save"}], "project": "default"}
$ curl "localhost:3984/api/spider-list?project=play"
{"success": true, "message": null, "spiders": [{"name": "ipip"}, {"name": "daili"}], "project": "dmhy"}
$ curl "localhost:3984/api/spider-list?project=my-project"
{"success": false, "message": "Project not find: my-project"}
```

#### 启动爬虫

- 请求地址：`/api/crawl`
- 请求方式：Post | Get
- 请求示例：

```shell
$ curl -XPOST 'http://localhost:2312/api/crawl?spider=ipip&project=dmhy' -d'{"spargs": {"keyword": "scrapy", "mode": "hello"}, "settings": {"DOWNLOAD_DELAY": 10}}'

{"job_id": "20200130_193440_Q9pfAl", "project": "dmhy", "spider": "ipip", "log_file": "/Users/mac/Git/spider/logs/scrapy_dmhy.spiders.ipip_spider_2020_1_30.log", "telnet": {"host": "127.0.0.1", "port": 6023, "username": "scrapy", "password": "c93fc576575bf2c8"}}
```

- 请求参数:

|请求参数|类型|是否允许为空|默认值|示例|说明|
|---|---|---|---|---|---|
|project| string | 是 | default| default | 指定爬虫所在项目|
|spider| string | 否 | - | ipip | 启动的爬虫名称 |
|spargs| object | 是 | {} | {"keyword": "scrapy", "mode": "hello"} | 爬虫传入的参数，等同于`scrapy crawl`的 -a, 不管使用POST还是GET都必须在请求体中 |
|settings| object | 是 | {} | {"DOWNLOAD_DELAY": 10} | 自定义scrapy settings配置，等同于`scrapy crawl`的 -a, 不管使用POST还是GET都必须在请求体中 |

- 响应结果：
```
{
    "job_id": "20200130_193440_Q9pfAl", 
    "project": "dmhy", 
    "spider": "ipip", 
    "log_file": "/Users/mac/Git/spider/logs/scrapy_dmhy.spiders.ipip_spider_2020_1_30.log", 
    "telnet": {
        "host": "127.0.0.1", 
        "port": 6023, 
        "username": "scrapy", 
        "password": "c93fc576575bf2c8"
    }
}
```

### 关闭爬虫

- 请求地址：`/api/stop`
- 请求方式：Get
- 请求示例：

```shell
$ curl 'http://localhost:2312/api/stop?job_id=20200201_182340_XJDfiY'

{"success": true, "project": "dmhy", "spider": "ipip", "message": "Finish", "status": "pending"}
```

- 请求参数：

|请求参数|类型|是否允许为空|默认值|示例|说明|
|---|---|---|---|---|---|
|job_id| string | 否 | - | 20200201_182340_XJDfiY | 请求的任务ID |

- 响应结果:

```
{
    "success": true, 
    "project": "dmhy", 
    "spider": "ipip", 
    "message": "Finish", 
    "status": "pending"
}
```

- status: 爬虫状态, pending表示正在关闭, close 表示已经关闭（可能telnet还未关闭，但是此时爬虫已经停止了）

### 修改默认配置
可以在项目根目录下创建`scrapycw_settings.py`文件来覆盖一些默认配置的值。可以覆盖的配置的值如下：

|配置项|类型|默认值|说明|
|---|---|---|---|
|SERVER_PORT| int | 2312 | web服务的默认端口号|
|SERVER_HOST| string| localhost|web服务允许访问的IP地址|
|SCRAPY_DEFAULT_PROJECT| string | default | scrapy默认项目|
|RUNTIME_PATH| string | scrapycw上级目录下的runtime_scrapycw | scrapycw运行中存储的内容目录|
|TELNET_TIMEOUT|int| 10 | telnet的超时时间，当为None是表示不设置超时时间(当关闭爬虫时，telnet会延后关闭，此时连接会超时)
