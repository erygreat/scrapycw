class MESSAGE_CODE:
    """
    响应码：
    0: 成功
    0 ~ 10000: 失败，但是结果是一致的
    10000 ~ 20000: 失败，没有找到资源
    20000 ~ 30000: 失败，传入参数错误
    30000 ~ 40000: 占位中，暂时没有使用
    40000 ~ 50000: 占位中，暂时没有使用
    """
    SUCCESS = 0

    FINISH_SPIDER_IS_CLOSE = 1

    FAIL_SPIDER_IS_CLOSE = 10001
    FAIL_CAN_NOT_FIND_SUB_COMMAND = 10002
    FAIL_CAN_NOT_FIND_JOB_ID = 10003
    FAIL_CAN_NOT_FIND_PROJECT = 10004
    FAIL_CAN_NOT_FIND_SPIDER = 10005

    NOT_ENTER_SPIDER_NAME = 20001
    