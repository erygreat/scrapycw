# Scrapycw

## 概述
Scrapycw是一个Scrapy监控程序，你可以通过命令行或者web服务的方式监控Scrapy爬虫运行情况，以及进行运行爬虫等常用操作。

## 依赖

- Python 3.5+
- 操作系统：Linux, Mac OSX, Windows

## 安装

在项目根目录下克隆项目 scrapycw
```
$ git clone git@github.com:erygreat/scrapycw.git
```
切换到release分支
```
$ cd scrapycw;
$ git checkout -b release origin/release
```

<font color="red">暂不支持通过pip安装（不久之后会支持,）</font>

## 使用方式

### 1. 命令行
可以使用 scrapycw 下的main.py脚本在控制台下运行命令

可用命令：

- projectlist
- spiderlist
- server

#### projectlist命令
语法：`python3 scrapycw/main.py projectlist`
说明：获取当前工作目录下所有的scrapy项目名称
示例：

```
$ python scrapycw/main.py projectlist
{'success': true, 'projects': [{'name': 'default'}, {'name': 'dmhy'}]}
```

#### spiderlist命令
语法：`python3 scrapycw/main.py spiderlist [-p <project>]`
说明：获取当前工作目录下某个scrapy项目下面所有爬虫的名称
属性：

- -p: scrapy项目名称，默认值为default

示例：

```
$ python scrapycw/main.py spiderlist -p dmhy
{'success': true, 'spiders': [{'name': 'ipip'}, {'name': 'daili'}], 'project': 'dmhy'}
```

#### server命令
语法：`python3 scrapycw/main.py server [<sub-command>] [--port <端口>] [--host <允许访问的地址>]`
说明：启动一个web服务，可以通过http请求获取scrapy服务信息
子命令:

- start: 开启web服务（默认值）
- stop: 关闭web服务
- restart: 重启web服务

属性：

start命令：

- --port：web服务端口，默认值为2312，可以通过覆盖 SERVER_PORT 修改默认值
- --host：web服务允许访问地址，默认值为localhost，如果设置为 0 表示完全开放，允许所有IP访问，可以通过覆盖 SERVER_HOST 修改默认值
- --daemon：后台启动web服务（开启一个守护进程）

示例：
```bash
$ # 开启一个web服务
$ python scrapycw/main.py server start --port 8080 --host 0 --daemon
start web service ...

$ python scrapycw/main.py server stop
stop web server...
关闭进程成功! 进程ID: 19572
关闭进程成功! 进程ID: 19581
关闭web service 完成

$ python scrapycw/main.py server stop --daemon
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
### 修改默认配置
可以在项目根目录下创建`scrapycw_settings.py`文件来覆盖一些默认配置的值。可以覆盖的配置的值如下：

|配置项|类型|默认值|说明|
|---|---|---|---|
|SERVER_PORT| int | 2312 | web服务的默认端口号|
|SERVER_HOST| string| localhost|web服务允许访问的IP地址|
|SCRAPY_DEFAULT_PROJECT| string | default | scrapy默认项目|
