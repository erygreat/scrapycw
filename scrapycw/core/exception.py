
from scrapycw.core.error_code import RESPONSE_CODE


class ScrapycwException(Exception):

    def __init__(self, message, code=RESPONSE_CODE.DEFAULT_ERROR, data=None, *args, **kwargs):
        super().__init__(message)
        self.message = message
        self.code = code
        self.data = data

    def __str__(self):
        return "[{}] {}".format(self.code, self.message)


class ScrapycwUsageException(ScrapycwException):
    pass


class ScrapycwDaemonProcessException(ScrapycwException):
    pass


class ScrapycwNotSupportSystemException(ScrapycwDaemonProcessException):
    pass


class ScrapycwCommandParamMissingException(ScrapycwDaemonProcessException):
    pass


class ScrapycwArgsMustCanSerializationException(ScrapycwDaemonProcessException):
    pass


class ScrapycwReadException(ScrapycwException):
    pass


class ScrapycwDaemonStartTimeoutException(ScrapycwDaemonProcessException):
    pass
