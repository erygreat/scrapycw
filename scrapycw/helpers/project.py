from scrapy.utils.conf import get_config
from scrapycw.helpers import Helper


class ProjectListHelper(Helper):

    def get(self):
        config = get_config()
        return [project for project, _ in config.items('settings')]
