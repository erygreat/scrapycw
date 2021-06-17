
class ScrapycwException(Exception):

    def __init__(self, code, message, data=None, *args, **kwargs):
        super().__init__(message)
        self.message = message
        self.code = code
        self.data = data


class ScrapycwUsageException(ScrapycwException):
    pass
