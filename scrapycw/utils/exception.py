
class ScrapycwException(Exception):

    def __init__(self, message):
        self.message = message


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
