from scrapycw.utils.slogger import get_logger


class classproperty(object):

    def __init__(self, fget):
        self.fget = fget

    def __get__(self, owner_self, owner_cls):
        return self.fget(owner_cls)


class ScrapycwObject():

    logger = None

    def __init__(self):
        self.logger = get_logger(self.__module__)

    @classproperty
    def logger(cls):
        return get_logger(cls.__module__)
