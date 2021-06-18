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

# server

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
