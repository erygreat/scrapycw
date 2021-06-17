Scrapycw是一个Scrapy监控程序，你可以通过命令行或者web服务的方式监控Scrapy爬虫运行情况，可以在网页上启动爬虫，以及在其他程序中通过调用接口的方式来监控爬虫运行情况。

## 支持环境

- Python 3.5+
- 操作系统：Linux, Mac OSX, Windows

## 安装

安装依赖包
```
$ pip3 install scrapycw
```

然后在命令行中运行
```
$ scrapycw version
```
如果出现了版本号表示安装成功！

## 项目初始化

在项目运行前需要进行初始化，在项目目录运行
```
$ scrapycw init
```
初始化项目

## 警告

注意：本项目依赖于scrapy的telnet，请不要使用 `TELNETCONSOLE_ENABLED` 配置禁用他。telnet本身是不安全的（即使有用户名和密码）因此响应的端口不应该对本机外开放，可以使用防火墙屏蔽掉这些端口。
另外 `TELNETCONSOLE_PASSWORD` 必须设置为None（自动生成密码）, 必须启动 `scrapy.extensions.telnet.TelnetConsole` 拓展。