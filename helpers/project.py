from scrapy.utils.conf import get_config

from scrapycw.helpers import Helper


class ProjectListHelper(Helper):

    def get_value(self):
        config = get_config()
        return [project for project, _ in config.items('settings')]

    def get_json(self):
        projects = []
        for project in self.get_value():
            projects.append({
                "name": project
            })
        return {
            "status": "success",
            "projects": projects,
        }
