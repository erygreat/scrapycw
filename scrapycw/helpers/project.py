from scrapy.utils.conf import get_config

from scrapycw.helpers import Helper


class ProjectHelper(Helper):

    def list(self):
        config = get_config()
        return [project for project, _ in config.items('settings')]
