from scrapycw.helpers.project import ScrapyProjectHelper


class ProjectHandler:

    @classmethod
    def list(cls):
        projects = []
        for project in ScrapyProjectHelper.list():
            projects.append({
                "name": project
            })
        return {
            "success": True,
            "projects": projects,
        }

