class ERROR_CODE:
    """
    响应码：
    0: 成功
    1 ~ 1000: 失败，但是结果是一致的
    1000 ~ 2000: 失败，没有找到资源
    2000 ~ 3000: 失败，传入参数错误
    """
    SUCCESS = 0

    # 爬虫已关闭
    FINISH_SPIDER_IS_CLOSE = 1

    # telnet 连接失败
    TELNET_NOT_CONNECT = 1000
    # telnet 授权失败，用户名或密码错误。
    TELNET_AUTHENTICATION_FAIL = 1001
    # telnet 连接被拒绝，没有该 Telnet
    TELNET_CONNECTION_REFUSED_ERROR = 1002
    # telnet 连接重置，该连接已关闭
    TELNET_CONNECTION_RESET_ERROR = 1003
    # telnet 连接超时
    TELNET_CONNECTION_TIMEOUT = 1004

    # 日志解析失败，不支持的时间格式
    LOG_PARSER_DONT_SUPPORT_DATA_FORMAT = 1010
    # 日志解析失败，没有找到该日志文件
    LOG_PARSER_LOG_NOT_FIND = 1011
    # 日志解析失败，日志文件过大无法解析
    LOG_PARSER_LOG_SIZE_MAXIMUM = 1012

    # 项目名称未找到
    PROJECT_NOT_FIND = 1020
    # 爬虫未找到
    SPIDER_NOT_FIND = 1021
    # 爬虫代码中存在BUG
    SPIDER_CODE_HAVE_BUG = 1022
    # job id没有找到
    JOB_ID_NOT_FIND = 1023
    # 启动爬虫超时
    SPIDER_RUN_TIMEOUT =1024

    # 爬虫已关闭
    FAIL_SPIDER_IS_CLOSE = 1030
    # 不支持的子命令
    NOT_SUPPORT_SUB_COMMAND = 1040
    # 不支持的操作系统
    NOT_SUPPORT_SYSTEM = 1050

    # 请输入爬虫名称
    NOT_ENTER_SPIDER_NAME = 2000
