
class ScrapycwException(Exception):

    def __init__(self, message, *args, **kwargs):
        super().__init__(message)
        self.message = message


class ScrapycwUsageException(ScrapycwException):
    pass
