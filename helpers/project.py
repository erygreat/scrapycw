from scrapy.utils.conf import get_config


class ScrapyProjectHelper:

    @classmethod
    def list(cls):
        config = get_config()
        return [project for project, _ in config.items('settings')]
