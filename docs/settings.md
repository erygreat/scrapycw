
# 修改默认配置

可以在`Scrapy`项目根目录下创建`scrapycw_settings.py`文件来覆盖一些默认配置的值。可以覆盖的配置的值如下：

**常用配置:**

| 配置项 | 类型 | 说明 | 默认值 |
| --- | --- | --- | --- |
| SERVER_PORT | int | Web 服务端口号 | 2312 |
| SERVER_HOST | string | web服务允许访问的IP地址 | localhost |
| SCRAPY_DEFAULT_PROJECT | string | Scrapy 默认项目 | default |
| HANDLE_LOG_MAXIMUM_SIZE | number | 处理的爬虫日志最大文件大小（当前处理日志会将整个日志加载到内存中，因此有此限制），单位为字节，默认为 500MB | 524288000 |
| HANDLE_LOG_USE_TIMEZONE | boolean | 处理日志时间时是否转化为本地时间（Scrapy使用的是 UTC） | True |
| LOGGING_LEVEL | number | Scrapycw 日志显示级别 | logging.DEBUG |

**其他配置**

| 配置项 | 类型 | 说明 | 默认值 |
| --- | --- | --- | --- |
| RUNTIME_PATH | string | Scrapycw 运行中存储的内容目录 | Scrapy 项目目录下的 runtime_scrapycw 文件夹 |
| SERVER_PID_FILENAME | string | 存储 Web 服务对应的 PID 数据文件文件名称 | `RUNTIME_PATH`配置路径下的`server.pid` 文件 |
| INIT_EACH_RUN | boolean | 每次运行命令时都会尝试初始化项目环境（后续会优化该问题） | False |
| TEMP_FILE_DIR | string | 爬虫运行时缓存文件目录 | `RUNTIME_PATH` 下的`temps`目录 |
| TELNET_TIMEOUT | number | Telnet 连接的超时时间，单位为秒，当为 None 时表示不设置超时时间(当关闭爬虫时，Telnet会延后关闭，此时连接会超时) | 10 |
| START_DAEMON_TIMEOUT | number |开启守护进程超时时间，单位为秒 | 30 |
| LOGGING_FILE | string | Scrapycw 日志文件名称 | `RUNTIME_PATH` 下的`log/scrapycw_%{当前日期}.log`文件 |
| LOGGING_FORMAT | string | scrapycw 日志格式 | '%(asctime)s [%(name)s] %(levelname)s: %(message)s' |
| SPIDER_LISTEN_LOOP_TIME | number | 检测爬虫是否正在运行心跳秒数 | 10 |