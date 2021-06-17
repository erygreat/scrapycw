# Scrapycw

Scrapycw是一个Scrapy监控程序，你可以通过命令行或者web服务的方式监控Scrapy爬虫运行情况，以及进行运行爬虫等常用操作。

- [安装](./docs/install.md)
- [命令行操作](./docs/commands.md)

注意：本项目依赖于scrapy的telnet，请不要使用`TELNETCONSOLE_ENABLED`配置禁用他。telnet本身是不安全的（即使有用户名和密码）因为响应的端口不应该对本机外开放，可以使用防火墙屏蔽掉这些端口。
另外`TELNETCONSOLE_PASSWORD`必须设置为None（自动生成密码）, 必须启动`scrapy.extensions.telnet.TelnetConsole`拓展。
