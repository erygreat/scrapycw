from scrapy.crawler import CrawlerProcess, CrawlerRunner
from scrapy.utils.log import configure_logging, log_scrapy_info
from scrapy.utils.ossignal import install_shutdown_handlers


class CustomCrawlerProcess(CrawlerProcess):
    def __init__(self, settings=None, install_root_handler=True):
        CrawlerRunner.__init__(self, settings)
        try:
            install_shutdown_handlers(self._signal_shutdown)
        except Exception:
            pass
        configure_logging(self.settings, install_root_handler)
        log_scrapy_info(self.settings)
