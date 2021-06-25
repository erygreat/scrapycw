import logging
import nanoid
from scrapycw.utils.slogger import get_logger
from scrapycw.settings import LOGGING_FILE


def test_sloger():
    log_1 = "hello_{}".format(nanoid.generate(size=12))
    log_2 = "world_{}".format(nanoid.generate(size=12))
    log_3 = "error_hello_{}".format(nanoid.generate(size=12))
    log_4 = "error_world_{}".format(nanoid.generate(size=12))

    slogger_info = get_logger("test_slogger_info", level=logging.INFO)
    slogger_info.error(log_1)
    slogger_info.info(log_2)

    slogger_error = get_logger("test_slogger_error", level=logging.ERROR)
    slogger_error.error(log_3)
    slogger_error.info(log_4)

    count = 0
    with open(LOGGING_FILE, "r") as file:
        for line in file:
            if line.find(log_1) != -1 or line.find(log_2) != -1 or line.find(log_3) != -1:
                count += 1
                assert(True)
            if line.find(log_4) != -1:
                count += 1
                assert(False)
    assert(count == 3)
            