from scrapy.utils.conf import get_config


class SpiderHandler:

    @classmethod
    def list(cls, project="default"):
        config = get_config()
        projects = []
        for project, _ in config.items('settings'):
            projects.append({
                "name": project
            })
        return {
            "success": True,
            "projects": projects,
        }
