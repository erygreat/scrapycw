from scrapycw.commands import ScrapycwCommand
from scrapycw.helpers.project import ProjectHelper


class Command(ScrapycwCommand):

    def run(self, args, opts):
        return ProjectHelper().list()

    def short_desc(self):
        return "List of project"

    def long_desc(self):
        return "List of project"
