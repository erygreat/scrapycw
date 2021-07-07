from scrapy.utils.conf import get_config

from scrapycw.helpers import SettingsHelper


class ProjectHelper(SettingsHelper):

    def list(self):
        config = get_config()
        return [project for project, _ in config.items('settings')]
