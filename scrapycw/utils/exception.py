
class ScrapycwException(Exception):

    def __init__(self, code, message, *args, **kwargs):
        super().__init__(message)
        self.message = message
        self.code = code


class ScrapycwUsageException(ScrapycwException):
    pass
