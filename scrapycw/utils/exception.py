
class ScrapycwException(Exception):

    def __init__(self, message):
        self.message = message


class ScrapycwUsageException(ScrapycwException):
    pass
