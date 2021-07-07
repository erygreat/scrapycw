# 命令行操作

可以在项目中运行`scrapycw -h`来获取可以使用的命令，包含许多子命令，子命令可以使用
```
scrapycw <command> -h
```
来获取详细的使用方式。

可用命令

- [init](#init)
- [version](#version)
- [server](#server)
- [projects](#projects)
- [spiders](#spiders)
- [crawl](#crawl)
- [pause](#pause)
- [unpause](#unpause)
- [stop](#stop)
- [jobs](#jobs)
- [job_stats](#job_stats)

除了`init`和`server`命令，都包含`pretty`参数来格式化输出，例如:
```
$ scrapycw projects --pretty
{
  "success": true,
  "message": null,
  "code": 0,
  "data": [
    "default",
    "demo",
    "project2",
    "new_project"
  ]
}
```

## init

语法：`scrapycw init`

说明：初始化 scrapycw，创建必须的文件，数据库等等，初次使用前必须运行该命令。

示例:
```
$ scrapycw init
```

## version

语法：`scrapycw version`

说明：获取当前 scrapycw 版本

示例：
```
$ scrapycw version
{"success": true, "message": null, "code": 0, "data": {"version": "0.3.0"}}
```

## server

语法: `scrapycw server <start|restart|stop> [options]`

说明：开启和关闭 Web 服务

示例:
**开启Web服务**
```
$ scrapycw server start
```

**关闭Web服务**
```
$ scrapycw server stop
```

**重启Web服务**
```
$ scrapycw server restart
```

**后台开启Web服务**
```
$ scrapycw server start --daemon
```

**指定端口号**
```
$ scrapycw server start --port=8080
```

## projects

语法：`scrapycw projects`

说明：获取项目列表

示例:
```
$ scrapycw projects
{"success": true, "message": null, "code": 0, "data": ["default", "demo", "project2", "new_project"]}
```

## spiders

语法：`scrapycw spiders [option]`

说明：获取爬虫列表

参数：

- project：显示的项目名称，如果没有设置该选项，则显示所有项目的所有爬虫列表

示例:
```
$ scrapycw spiders
{"success": true, "message": null, "code": 0, "data": [{"project": "default", "spiders": ["baidu"]}, {"project": "demo", "spiders": []}, {"project": "project2", "spiders": []}, {"project": "new_project", "spiders": []}]}

$ scrapycw spiders -p default
{"success": true, "message": null, "code": 0, "data": {"spiders": ["baidu"], "project": "default"}}
```
## crawl

语法：`scrapycw crawl <spider-name> [option]`

说明：启动爬虫

参数：

- project：爬虫所在项目名称, 默认值为默认项目
- s：手动设置settings值，同 Scrapy
- a：手动设置爬虫参数，同 Scrapy

示例:
```
$ scrapycw crawl baidu

{"success": true, "message": null, "code": 0, "data": {"job_id": "20210629_203543_un6_ITAgoDWk", "project": "default", "spider": "baidu", "log_file": null, "telnet": {"host": "127.0.0.1", "port": 6023, "username": "scrapy", "password": "ef434708f541b17e"}}}
```

## pause

语法: `scrapycw pause <job_id>`

说明: 使目标爬虫任务暂停

示例:
```
$ scrapycw pause 20210629_203543_un6_ITAgoDWk
{"success": false, "message": "由于目标计算机积极拒绝，无法连接。", "code": 1002, "data": {"status": "closed"}}

$ scrapycw pause 20210705_194355_v_kmpbHIDJXi
{"success": true, "message": null, "code": 0, "data": {"status": "paused"}}
```

## pause

语法: `scrapycw unpause <job_id>`

说明: 取消目标爬虫任务暂停

示例:
```
$ scrapycw unpause 20210629_203543_un6_ITAgoDWk
{"success": false, "message": "由于目标计算机积极拒绝，无法连接。", "code": 1002, "data": {"status": "closed"}}

$ scrapycw pause 20210705_194355_v_kmpbHIDJXi
{"success": true, "message": null, "code": 0, "data": {"status": "paused"}}

$ scrapycw unpause 20210705_194355_v_kmpbHIDJXi
{"success": true, "message": null, "code": 0, "data": {"status": "running"}}
```

## stop

语法: `scrapycw stop <job_id>`

说明: 停止目标爬虫

示例:
```
$ scrapycw unpause 20210629_203543_un6_ITAgoDWk
{"success": false, "message": "由于目标计算机积极拒绝，无法连接。", "code": 1002, "data": {"status": "closed"}}

$ scrapycw unpause 20210705_194355_v_kmpbHIDJXi
{"success": true, "message": null, "code": 0, "data": {"status": "running"}}
```

## jobs

语法: `scrapycw jobs [options]`

说明: 获取爬虫信息列表

参数:

- `offset`: 列表起始下标，默认为0
- `limit`: 查询长度, 默认为10
- `project`: 查询的项目名称，默认查询所有项目
- `spider`: 默认查询的爬虫名称，默认查询所有爬虫
- `status`: 查询的爬虫状态，可选状态为: ('running', 'closed')
- `close-reason`: 查询的关闭原因，常用的原因包括 ['unknown', 'finished','shutdown'], 也可以使用自定义原因，例如: 'canceled'

示例:
```
$ scrapycw jobs --limit 1
{
  "success": true,
  "message": null,
  "code": 0,
  "data": {
    "jobs": [
      {
        "job_id": "20210707_152905_bc84bb3lFfIO",
        "project": "default",
        "spider": "baidu_log",
        "telnet": {
          "username": "scrapy",
          "password": "ead0f64950b7353b",
          "host": "127.0.0.1",
          "port": 6023
        },
        "status": "closed",
        "start_time": "2021-07-07 15:29:05",
        "end_time": "2021-07-07 15:29:08",
        "close_reason": "shutdown",
        "page_count": 1,
        "item_count": 0,
        "created_time": "2021-07-07 15:29:05",
        "updated_time": "2021-07-07 15:29:20"
      }
    ],
    "offset": 0,
    "limit": 1,
    "count": 9
  }
}

$ scrapycw jobs --limit 1 --spider ip_taobao --pretty
{
  "success": true,
  "message": null,
  "code": 0,
  "data": {
    "jobs": [
      {
        "job_id": "20210707_152744_Nk101FhsMJUJ",
        "project": "default",
        "spider": "ip_taobao",
        "telnet": {
          "username": "scrapy",
          "password": "70e6e2838f24f8f0",
          "host": "127.0.0.1",
          "port": 6023
        },
        "status": "closed",
        "start_time": "2021-07-07 15:27:44",
        "end_time": "2021-07-07 15:27:44",
        "close_reason": "finished",
        "page_count": 1,
        "item_count": 1,
        "created_time": "2021-07-07 15:27:44",
        "updated_time": "2021-07-07 15:27:50"
      }
    ],
    "offset": 0,
    "limit": 1,
    "count": 3
  }
}
```
> 注意，当前返回的`status`目前不包含4种：`closed`, `running`, `paused`, `closing`


## job_stats

语法: `scrapycw job_stats <job-id> [options]`

说明: 获取爬虫详细信息

参数:

- `settings`: 是否输出settings
- `log`: 是否输出日志信息
- `stats`: 是否输出任务stats信息
- `est`: 是否输出运行时 est 信息 (如果任务没有运行，则输出 None)

示例:
```
$ scrapycw job_stats 20210707_162315_0yIddAGU-zRh --pretty
{
  "success": true,
  "message": null,
  "code": 0,
  "data": {
    "job_id": "20210707_162315_0yIddAGU-zRh",
    "project": "default",
    "spider": "baidu_log",
    "log_path": "C:\\Users\\L13\\git\\scrapycw_test_project\\logs\\baidu-have-log.log",
    "start_time": "2021-07-07 16:23:15",
    "end_time": "2021-07-07 16:23:17",
    "closed_reason": "shutdown",
    "pages": 1,
    "items": 0,
    "runtime": "0:00:02",
    "status": "closed"
  }
}

$ scrapycw job_stats 20210707_162315_0yIddAGU-zRh --stats --pretty
{
  "success": true,
  "message": null,
  "code": 0,
  "data": {
    "job_id": "20210707_162315_0yIddAGU-zRh",
    "project": "default",
    "spider": "baidu_log",
    "log_path": "C:\\Users\\L13\\git\\scrapycw_test_project\\logs\\baidu-have-log.log",
    "start_time": "2021-07-07 16:23:15",
    "end_time": "2021-07-07 16:23:17",
    "closed_reason": "shutdown",
    "pages": 1,
    "items": 0,
    "runtime": "0:00:02",
    "status": "closed",
    "stats": {
      "downloader/request_bytes": 422,
      "downloader/request_count": 2,
      "downloader/request_method_count/GET": 2,
      "downloader/response_bytes": 1838,
      "downloader/response_count": 2,
      "downloader/response_status_count/200": 2,
      "elapsed_time_seconds": 2.124792,
      "finish_reason": "shutdown",
      "finish_time": "2021-07-07 08:23:17",
      "httpcompression/response_bytes": 2381,
      "httpcompression/response_count": 1,
      "log_count/DEBUG": 2,
      "log_count/INFO": 10,
      "request_depth_max": 1,
      "response_received_count": 1,
      "scheduler/dequeued": 2,
      "scheduler/dequeued/memory": 2,
      "scheduler/enqueued": 3,
      "scheduler/enqueued/memory": 3,
      "start_time": "2021-07-07 08:23:15"
    }
  }
}
```