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