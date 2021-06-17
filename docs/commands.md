# 命令行操作

可以在项目中运行`scrapycw -h`来获取可以使用的命令，包含许多子命令，子命令可以使用
```
scrapycw <command> -h
```
来获取详细的使用方式。

可用命令

- [init](#init)
- [version](#version)

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