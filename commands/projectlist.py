from scrapycw.commands import ScrapycwCommand
from scrapycw.helpers.project import ProjectListHelper


class Command(ScrapycwCommand):

    def run(self, args, opts):
        return ProjectListHelper().get_json()

    def short_desc(self):
        return "List of project"

    def long_desc(self):
        return "List of project"
