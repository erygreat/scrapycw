from scrapy.utils.conf import get_config

from scrapycw.helpers import Helper


class ProjectHelper(Helper):

    def list(self):
        config = get_config()
        return {
            "success": True,
            "message": None,
            "projects": [project for project, _ in config.items('settings')],
        }
