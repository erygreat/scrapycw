
class ScrapycwException(Exception):

    def __init__(self, code, message, data=None, *args, **kwargs):
        super().__init__(message)
        self.message = message
        self.code = code
        self.data = data

    def __str__(self) -> str:
        return "[{}] {}".format(self.code, self.message)


class ScrapycwUsageException(ScrapycwException):
    pass
